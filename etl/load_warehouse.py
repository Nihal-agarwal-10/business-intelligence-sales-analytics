
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# ============================================================
# 1. CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

required_vars = [
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
]

missing_vars = [key for key in required_vars if not os.getenv(key)]

if missing_vars:
    raise ValueError(
        f"Missing environment variables in .env: {', '.join(missing_vars)}"
    )

database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(database_url, pool_pre_ping=True)


# ============================================================
# 2. HELPER: CHECK TABLE EXISTS
# ============================================================

def table_exists(conn, table_name):
    return conn.execute(
        text("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_name = :table_name
            )
        """),
        {"table_name": table_name},
    ).scalar_one()


# ============================================================
# 3. LOAD WAREHOUSE
# ============================================================

def load_warehouse():
    with engine.begin() as conn:
        staging_tables = [
            "staging_customers",
            "staging_products",
            "staging_orders",
        ]

        warehouse_tables = [
            "dim_customer",
            "dim_product",
            "dim_date",
            "dim_sales_channel",
            "fact_sales",
        ]

        # ----------------------------------------------------
        # Validate required tables
        # ----------------------------------------------------

        for table in staging_tables:
            if not table_exists(conn, table):
                raise RuntimeError(
                    f"Missing staging table: {table}. "
                    "Run etl/load_data.py first."
                )

        for table in warehouse_tables:
            if not table_exists(conn, table):
                raise RuntimeError(
                    f"Missing warehouse table: {table}. "
                    "Run sql/schema.sql first."
                )

        # ----------------------------------------------------
        # Validate staging data
        # ----------------------------------------------------

        invalid_orders = conn.execute(text("""
            SELECT COUNT(*)
            FROM staging_orders o
            LEFT JOIN staging_customers c
                ON c.customer_id = o.customer_id
            LEFT JOIN staging_products p
                ON p.product_id = o.product_id
            WHERE c.customer_id IS NULL
               OR p.product_id IS NULL
               OR o.order_id IS NULL
               OR o.order_date IS NULL
               OR o.quantity IS NULL
               OR o.quantity <= 0
               OR o.sales_channel IS NULL
        """)).scalar_one()

        if invalid_orders:
            raise RuntimeError(
                f"{invalid_orders} staging orders have invalid "
                "required values or missing customer/product records."
            )

        duplicate_orders = conn.execute(text("""
            SELECT COUNT(*)
            FROM (
                SELECT order_id
                FROM staging_orders
                GROUP BY order_id
                HAVING COUNT(*) > 1
            ) duplicates
        """)).scalar_one()

        if duplicate_orders:
            raise RuntimeError(
                f"Found {duplicate_orders} duplicate order IDs "
                "in staging_orders. Resolve them before loading."
            )

        # ----------------------------------------------------
        # 1. CUSTOMER DIMENSION
        # ----------------------------------------------------

        conn.execute(text("""
            INSERT INTO dim_customer (
                customer_id,
                customer_name,
                region,
                country,
                industry,
                customer_segment
            )
            SELECT
                customer_id,
                customer_name,
                region,
                country,
                industry,
                customer_segment
            FROM staging_customers
            ON CONFLICT (customer_id) DO NOTHING
        """))

        # ----------------------------------------------------
        # 2. PRODUCT DIMENSION
        # ----------------------------------------------------

        conn.execute(text("""
            INSERT INTO dim_product (
                product_id,
                product_name,
                category,
                sub_category,
                unit_price,
                unit_cost
            )
            SELECT
                product_id,
                product_name,
                category,
                sub_category,
                unit_price,
                unit_cost
            FROM staging_products
            ON CONFLICT (product_id) DO NOTHING
        """))

        # ----------------------------------------------------
        # 3. SALES CHANNEL DIMENSION
        # ----------------------------------------------------

        conn.execute(text("""
            INSERT INTO dim_sales_channel (sales_channel)
            SELECT DISTINCT sales_channel
            FROM staging_orders
            WHERE sales_channel IS NOT NULL
            ON CONFLICT (sales_channel) DO NOTHING
        """))

        # ----------------------------------------------------
        # 4. DATE DIMENSION
        # ----------------------------------------------------

        conn.execute(text("""
            INSERT INTO dim_date (
                date_key,
                full_date,
                year,
                quarter,
                month,
                month_name,
                week_number
            )
            SELECT
                TO_CHAR(d::date, 'YYYYMMDD')::INTEGER,
                d::date,
                EXTRACT(YEAR FROM d)::INTEGER,
                EXTRACT(QUARTER FROM d)::INTEGER,
                EXTRACT(MONTH FROM d)::INTEGER,
                TO_CHAR(d::date, 'FMMonth'),
                EXTRACT(WEEK FROM d)::INTEGER
            FROM (
                SELECT generate_series(
                    MIN(order_date::date),
                    MAX(order_date::date),
                    INTERVAL '1 day'
                ) AS d
                FROM staging_orders
            ) dates
            ON CONFLICT (date_key) DO NOTHING
        """))

        # ----------------------------------------------------
        # Validate dimension mappings before inserting facts
        # ----------------------------------------------------

        unmatched_orders = conn.execute(text("""
            SELECT COUNT(*)
            FROM staging_orders o
            LEFT JOIN dim_customer c
                ON c.customer_id = o.customer_id
            LEFT JOIN dim_product p
                ON p.product_id = o.product_id
            LEFT JOIN dim_sales_channel sc
                ON sc.sales_channel = o.sales_channel
            LEFT JOIN dim_date d
                ON d.full_date = o.order_date::date
            WHERE c.customer_key IS NULL
               OR p.product_key IS NULL
               OR sc.channel_key IS NULL
               OR d.date_key IS NULL
        """)).scalar_one()

        if unmatched_orders:
            raise RuntimeError(
                f"{unmatched_orders} orders cannot be mapped to "
                "all warehouse dimensions. Transaction rolled back."
            )

        # ----------------------------------------------------
        # 5. FACT TABLE
        # ----------------------------------------------------

        result = conn.execute(text("""
            INSERT INTO fact_sales (
                order_id,
                date_key,
                customer_key,
                product_key,
                channel_key,
                quantity,
                revenue,
                cost,
                profit
            )
            SELECT
                o.order_id,
                d.date_key,
                c.customer_key,
                p.product_key,
                sc.channel_key,
                o.quantity,
                ROUND(o.quantity * p.unit_price, 2),
                ROUND(o.quantity * p.unit_cost, 2),
                ROUND(
                    o.quantity * (p.unit_price - p.unit_cost),
                    2
                )
            FROM staging_orders o
            JOIN dim_customer c
                ON c.customer_id = o.customer_id
            JOIN dim_product p
                ON p.product_id = o.product_id
            JOIN dim_sales_channel sc
                ON sc.sales_channel = o.sales_channel
            JOIN dim_date d
                ON d.full_date = o.order_date::date
            WHERE NOT EXISTS (
                SELECT 1
                FROM fact_sales f
                WHERE f.order_id = o.order_id
            )
        """))

        inserted_rows = result.rowcount

        # ----------------------------------------------------
        # 6. REPORT COUNTS
        # ----------------------------------------------------

        print("\nWAREHOUSE LOAD SUMMARY")
        print("=" * 40)

        for table in warehouse_tables:
            row_count = conn.execute(
                text(f"SELECT COUNT(*) FROM public.{table}")
            ).scalar_one()

            print(f"{table}: {row_count:,} rows")

        print(f"\nNew fact rows inserted: {inserted_rows:,}")

    # Reaching this point means the transaction committed.
    print("\nWarehouse load completed successfully.")


# ============================================================
# 4. EXECUTION
# ============================================================

if __name__ == "__main__":
    try:
        load_warehouse()
    except Exception as exc:
        print(f"\nWAREHOUSE LOAD FAILED: {exc}")
        raise
    finally:
        engine.dispose()
