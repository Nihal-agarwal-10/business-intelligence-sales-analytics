# Business Intelligence Sales Analytics Platform

An end-to-end Business Intelligence project that transforms raw sales data into analytical insights using Python, PostgreSQL, SQL, and Power BI.

## Project Overview

This project demonstrates a complete BI workflow, from synthetic data generation and data cleaning to warehouse loading, SQL analysis, and interactive dashboard development.

The dataset contains 50,000 orders, 2,000 customers, and 100 products, covering January 2024 to September 2026.

**Note:** The dataset is synthetic and is intended for portfolio and demonstration purposes. It does not represent real company sales.

## Technology Stack

- **Python:** Data generation, cleaning, and ETL
- **Pandas:** Data manipulation and preprocessing
- **PostgreSQL:** Relational database and analytical warehouse
- **SQL:** Data transformations and business analysis
- **Power BI:** Interactive dashboards and visual reporting
- **DAX:** KPI calculations and analytical measures
- **Git and GitHub:** Version control and project hosting

## Project Architecture

```text
Synthetic Sales Data
        |
        v
Python + Pandas
Data Generation and Cleaning
        |
        v
PostgreSQL Staging Tables
        |
        v
Dimensional Data Warehouse
        |
        v
SQL Analytics and DAX Measures
        |
        v
Power BI Dashboards
```

## Repository Structure

```text
Business-Intelligence-Sales-Analytics/
├── data/
│   ├── raw/
│   └── processed/
├── etl/
│   ├── generate_data.py
│   ├── create_data_issues.py
│   ├── clean_data.py
│   └── load_data.py
├── notebooks/
├── powerbi/
│   └── sales_analytics.pbix
├── sql/
│   ├── schema.sql
│   └── analytics.sql
├── .gitignore
├── requirements.txt
└── README.md
```

Generated CSV files and environment credentials are excluded from version control.

## Data Engineering and ETL

The ETL workflow includes:

1. Generating synthetic customers, products, orders, and returns.
2. Introducing data-quality issues for cleaning demonstrations.
3. Cleaning datasets, including handling missing values, duplicate records, and inconsistent categorical values.
4. Loading cleaned customer, product, and order data into PostgreSQL staging tables.
5. Transforming staging data into dimensional tables and the sales fact table.

## Data Warehouse

The warehouse follows a star-schema design.

**Dimension tables**
- `dim_customer`
- `dim_product`
- `dim_date`
- `dim_sales_channel`

**Fact table**
- `fact_sales`

The fact table stores order-level sales measures, including quantity, revenue, cost, and profit. Dimension tables provide customer, product, date, and sales-channel context for analysis.

## Power BI Dashboards

### 1. Executive Overview

Provides a consolidated view of business performance through:
- Total Revenue
- Total Profit
- Profit Margin
- Total Orders
- Total Customers
- Average Order Value
- Monthly Revenue Trend
- Revenue by Region
- Revenue by Product Category

Includes slicers for year, region, and product category.

### 2. Product Analytics

Provides product-level analysis through:
- Top 10 Products by Revenue
- Revenue by Product Category
- Top 10 Products by Profit
- Product Details table with pricing, cost, revenue, and profit
- Year and category slicers

## Key Measures

The report includes DAX measures for revenue, cost, profit, profit margin, order count, customer count, and average order value.

Example:

```dax
Profit Margin =
DIVIDE([Total Profit], [Total Revenue], 0)
```

```dax
Average Order Value =
DIVIDE([Total Revenue], [Total Orders], 0)
```

## SQL Validation

The warehouse was validated against aggregate SQL results.

| Metric | Validated result |
|---|---:|
| Fact table rows | 50,000 |
| Distinct order IDs | 50,000 |
| Total Revenue | 8,861,619,904.35 |
| Total Profit | 2,423,578,378.12 |
| Profit Margin | 27.35% |

These values are derived from the synthetic dataset and are not real business results.

## Running the Project

### Prerequisites

- Python
- PostgreSQL
- Power BI Desktop
- Git

### Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies from `requirements.txt`.
4. Configure a local `.env` file with the PostgreSQL connection settings expected by the ETL script.
5. Create the database and run the SQL schema script.
6. Generate and clean the datasets.
7. Load the cleaned data into PostgreSQL.
8. Run the analytical SQL queries.
9. Open `powerbi/sales_analytics.pbix` in Power BI Desktop and configure the data connection for your environment.

Run the ETL scripts from the project root in the appropriate order:

```bash
python etl/generate_data.py
python etl/create_data_issues.py
python etl/clean_data.py
python etl/load_data.py
```

Run the SQL scripts in `sql/` using your PostgreSQL client. Follow any connection and schema setup requirements in the scripts.

## Learning Outcomes

This project demonstrates practical experience with:
- Data cleaning and quality checks
- Python-based ETL workflows
- Relational database design
- Dimensional modeling and star schemas
- SQL aggregations and business analytics
- DAX measures and interactive Power BI reporting
- Git-based project version control

## Limitations

- The data is synthetic rather than sourced from a real organization.
- The project uses a local PostgreSQL environment; connection settings must be configured by each user.
- Cloud ETL services such as Azure Data Factory and Azure Synapse are not implemented in this version.

## Future Improvements

- Add customer segmentation and retention analysis.
- Automate ETL execution and data-quality testing.
- Add additional dashboard pages and deeper trend analysis.
- Extend the pipeline to a cloud data platform.

---

**Author:** Nihal Agarwal  
**Project:** Business Intelligence Sales Analytics Platform