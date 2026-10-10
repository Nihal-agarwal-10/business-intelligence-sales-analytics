import pandas as pd
from pathlib import Path

# -----------------------------
# Project paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# 1. Load raw data
# -----------------------------

customers = pd.read_csv(
    RAW_DIR / "customers_messy.csv"
)

products = pd.read_csv(
    RAW_DIR / "products.csv"
)

orders = pd.read_csv(
    RAW_DIR / "orders.csv"
)

returns = pd.read_csv(
    RAW_DIR / "returns.csv"
)

print("Raw datasets loaded.")

# ============================================================
# CUSTOMER DATA CLEANING
# ============================================================

print("\nCleaning customer data...")

# Remove duplicate customer IDs
customers = customers.drop_duplicates(
    subset=["customer_id"],
    keep="first"
)

# Fill missing industry values
customers["industry"] = customers["industry"].fillna(
    "Unknown"
)

# Standardize region values
customers["region"] = (
    customers["region"]
    .astype(str)
    .str.strip()
    .str.title()
)

# Remove unnecessary whitespace from customer names
customers["customer_name"] = (
    customers["customer_name"]
    .astype(str)
    .str.strip()
)

# ============================================================
# PRODUCT DATA CLEANING
# ============================================================

print("Cleaning product data...")

products["product_name"] = (
    products["product_name"]
    .astype(str)
    .str.strip()
)

products["category"] = (
    products["category"]
    .astype(str)
    .str.strip()
    .str.title()
)

products["sub_category"] = (
    products["sub_category"]
    .astype(str)
    .str.strip()
)

# Make sure prices are numeric
products["unit_price"] = pd.to_numeric(
    products["unit_price"],
    errors="coerce"
)

products["unit_cost"] = pd.to_numeric(
    products["unit_cost"],
    errors="coerce"
)

# Remove products with invalid prices
products = products.dropna(
    subset=["unit_price", "unit_cost"]
)

# ============================================================
# ORDER DATA CLEANING
# ============================================================

print("Cleaning order data...")

# Convert order date to datetime
orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

# Convert quantity to numeric
orders["quantity"] = pd.to_numeric(
    orders["quantity"],
    errors="coerce"
)

# Remove orders with missing critical fields
orders = orders.dropna(
    subset=[
        "order_id",
        "order_date",
        "customer_id",
        "product_id",
        "quantity"
    ]
)

# Keep only positive quantities
orders = orders[
    orders["quantity"] > 0
]

# Make quantity an integer
orders["quantity"] = orders["quantity"].astype(int)

# Standardize sales channel
orders["sales_channel"] = (
    orders["sales_channel"]
    .astype(str)
    .str.strip()
    .str.title()
)

# ============================================================
# RETURN DATA CLEANING
# ============================================================

print("Cleaning return data...")

returns["return_date"] = pd.to_datetime(
    returns["return_date"],
    errors="coerce"
)

returns["return_quantity"] = pd.to_numeric(
    returns["return_quantity"],
    errors="coerce"
)

# Remove invalid return records
returns = returns.dropna(
    subset=[
        "return_id",
        "order_id",
        "return_date",
        "return_quantity"
    ]
)

# Keep only positive return quantities
returns = returns[
    returns["return_quantity"] > 0
]

returns["return_quantity"] = (
    returns["return_quantity"]
    .astype(int)
)

returns["return_reason"] = (
    returns["return_reason"]
    .astype(str)
    .str.strip()
)

# ============================================================
# SAVE CLEAN DATA
# ============================================================

customers.to_csv(
    PROCESSED_DIR / "customers_clean.csv",
    index=False
)

products.to_csv(
    PROCESSED_DIR / "products_clean.csv",
    index=False
)

orders.to_csv(
    PROCESSED_DIR / "orders_clean.csv",
    index=False
)

returns.to_csv(
    PROCESSED_DIR / "returns_clean.csv",
    index=False
)

# ============================================================
# VALIDATION / SUMMARY
# ============================================================

print("\nData cleaning complete.")

print(f"Customers after cleaning: {len(customers)}")
print(f"Products after cleaning: {len(products)}")
print(f"Orders after cleaning: {len(orders)}")
print(f"Returns after cleaning: {len(returns)}")

print(f"\nClean files saved to:")
print(PROCESSED_DIR)