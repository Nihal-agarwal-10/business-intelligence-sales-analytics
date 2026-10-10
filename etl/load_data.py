import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Database credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# PostgreSQL connection
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# Read cleaned CSV files
customers = pd.read_csv(DATA_DIR / "customers_clean.csv")
products = pd.read_csv(DATA_DIR / "products_clean.csv")
orders = pd.read_csv(DATA_DIR / "orders_clean.csv")

# Load data into staging tables
customers.to_sql(
    "staging_customers",
    engine,
    if_exists="replace",
    index=False
)

products.to_sql(
    "staging_products",
    engine,
    if_exists="replace",
    index=False
)

orders.to_sql(
    "staging_orders",
    engine,
    if_exists="replace",
    index=False
)

print("Data loaded into PostgreSQL staging tables.")
print(f"Customers loaded: {len(customers)}")
print(f"Products loaded: {len(products)}")
print(f"Orders loaded: {len(orders)}")