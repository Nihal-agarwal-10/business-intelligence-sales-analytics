-- ==========================================
-- BUSINESS INTELLIGENCE SALES ANALYTICS
-- DATA WAREHOUSE SCHEMA
-- ==========================================


-- ==========================================
-- 1. CUSTOMER DIMENSION
-- ==========================================

CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(20) UNIQUE NOT NULL,
    customer_name VARCHAR(255),
    region VARCHAR(50),
    country VARCHAR(100),
    industry VARCHAR(100),
    customer_segment VARCHAR(50)
);


-- ==========================================
-- 2. PRODUCT DIMENSION
-- ==========================================

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(20) UNIQUE NOT NULL,
    product_name VARCHAR(255),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    unit_price NUMERIC(12,2),
    unit_cost NUMERIC(12,2)
);


-- ==========================================
-- 3. DATE DIMENSION
-- ==========================================

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    week_number INTEGER
);


-- ==========================================
-- 4. SALES CHANNEL DIMENSION
-- ==========================================

CREATE TABLE dim_sales_channel (
    channel_key SERIAL PRIMARY KEY,
    sales_channel VARCHAR(50) UNIQUE NOT NULL
);


-- ==========================================
-- 5. SALES FACT TABLE
-- ==========================================

CREATE TABLE fact_sales (
    sales_key BIGSERIAL PRIMARY KEY,

    order_id VARCHAR(30) NOT NULL,

    date_key INTEGER
        REFERENCES dim_date(date_key),

    customer_key INTEGER
        REFERENCES dim_customer(customer_key),

    product_key INTEGER
        REFERENCES dim_product(product_key),

    channel_key INTEGER
        REFERENCES dim_sales_channel(channel_key),

    quantity INTEGER,

    revenue NUMERIC(14,2),

    cost NUMERIC(14,2),

    profit NUMERIC(14,2)
);