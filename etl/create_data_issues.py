import pandas as pd
from pathlib import Path
import random

# -----------------------------
# Project paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

# -----------------------------
# Load raw customer data
# -----------------------------

customers = pd.read_csv(RAW_DIR / "customers.csv")

# -----------------------------
# 1. Introduce missing values
# -----------------------------

missing_indices = customers.sample(
    frac=0.01,
    random_state=42
).index

customers.loc[missing_indices, "industry"] = None

# -----------------------------
# 2. Introduce inconsistent region values
# -----------------------------

south_indices = customers[
    customers["region"] == "South"
].sample(
    frac=0.02,
    random_state=42
).index

customers.loc[south_indices, "region"] = "south "

# -----------------------------
# 3. Introduce duplicate records
# -----------------------------

duplicates = customers.sample(
    n=20,
    random_state=42
)

customers_messy = pd.concat(
    [customers, duplicates],
    ignore_index=True
)

# -----------------------------
# Save messy dataset
# -----------------------------

customers_messy.to_csv(
    RAW_DIR / "customers_messy.csv",
    index=False
)

# -----------------------------
# Completion message
# -----------------------------

print("Data quality issues introduced successfully.")

print(f"Original customer records: {len(customers)}")
print(f"Messy customer records: {len(customers_messy)}")
print(
    f"Duplicate records introduced: "
    f"{len(customers_messy) - len(customers)}"
)

print(
    f"Missing industry values: "
    f"{customers_messy['industry'].isna().sum()}"
)

print("\nCreated:")
print(RAW_DIR / "customers_messy.csv")