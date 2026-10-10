import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path
import random

# -----------------------------
# Project paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Configuration
# -----------------------------

NUM_CUSTOMERS = 2000
NUM_PRODUCTS = 100
NUM_ORDERS = 50000

fake = Faker()
random.seed(42)
np.random.seed(42)

# -----------------------------
# 1. Generate Customers
# -----------------------------

customers = []

regions = ["North", "South", "East", "West"]

industries = [
    "Manufacturing",
    "Retail",
    "Healthcare",
    "Automotive",
    "Construction",
    "Technology"
]

customer_segments = [
    "Enterprise",
    "Mid-Market",
    "SMB"
]

for i in range(1, NUM_CUSTOMERS + 1):

    customers.append({
        "customer_id": f"CUST{i:05d}",
        "customer_name": fake.company(),
        "region": random.choice(regions),
        "country": "India",
        "industry": random.choice(industries),
        "customer_segment": random.choice(customer_segments)
    })

customers_df = pd.DataFrame(customers)

# -----------------------------
# 2. Generate Products
# -----------------------------

products = []

categories = {
    "Materials": [
        "Polymers",
        "Resins",
        "Coatings"
    ],
    "Specialty": [
        "Adhesives",
        "Performance Additives",
        "Specialty Chemicals"
    ],
    "Industrial": [
        "Industrial Solutions",
        "Processing Materials",
        "Engineering Materials"
    ]
}

for i in range(1, NUM_PRODUCTS + 1):

    category = random.choice(list(categories.keys()))
    sub_category = random.choice(categories[category])

    unit_cost = round(random.uniform(100, 5000), 2)
    unit_price = round(
        unit_cost * random.uniform(1.15, 1.60),
        2
    )

    products.append({
        "product_id": f"PROD{i:04d}",
        "product_name": f"{sub_category} Product {i}",
        "category": category,
        "sub_category": sub_category,
        "unit_price": unit_price,
        "unit_cost": unit_cost
    })

products_df = pd.DataFrame(products)

# -----------------------------
# 3. Generate Orders
# -----------------------------

order_dates = pd.date_range(
    start="2024-01-01",
    end="2026-09-30",
    freq="D"
)

orders = []

sales_channels = [
    "Direct",
    "Distributor",
    "Online"
]

for i in range(1, NUM_ORDERS + 1):

    orders.append({
        "order_id": f"ORD{i:06d}",
        "order_date": random.choice(order_dates),
        "customer_id": random.choice(
            customers_df["customer_id"].tolist()
        ),
        "product_id": random.choice(
            products_df["product_id"].tolist()
        ),
        "quantity": random.randint(1, 99),
        "sales_channel": random.choice(sales_channels)
    })

orders_df = pd.DataFrame(orders)

# -----------------------------
# 4. Generate Returns
# -----------------------------

returns = []

return_reasons = [
    "Damaged",
    "Quality Issue",
    "Wrong Product",
    "Customer Changed Mind"
]

for _, order in orders_df.iterrows():

    # Approximately 4% of orders are returned
    if random.random() < 0.04:

        return_quantity = random.randint(
            1,
            int(order["quantity"])
        )

        returns.append({
            "return_id": f"RET{len(returns) + 1:05d}",
            "order_id": order["order_id"],
            "return_date": order["order_date"],
            "return_quantity": return_quantity,
            "return_reason": random.choice(return_reasons)
        })

returns_df = pd.DataFrame(returns)

# -----------------------------
# 5. Save CSV files
# -----------------------------

customers_df.to_csv(
    RAW_DIR / "customers.csv",
    index=False
)

products_df.to_csv(
    RAW_DIR / "products.csv",
    index=False
)

orders_df.to_csv(
    RAW_DIR / "orders.csv",
    index=False
)

returns_df.to_csv(
    RAW_DIR / "returns.csv",
    index=False
)

# -----------------------------
# 6. Completion message
# -----------------------------

print("Data generation complete.")

print(f"Customers: {len(customers_df)}")
print(f"Products: {len(products_df)}")
print(f"Orders: {len(orders_df)}")
print(f"Returns: {len(returns_df)}")

print(f"\nFiles saved to: {RAW_DIR}")