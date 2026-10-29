# Business Intelligence Sales Analytics Platform

A complete end-to-end Business Intelligence project that transforms raw sales data into a structured PostgreSQL data warehouse and interactive Power BI dashboards. The project demonstrates data generation, data cleaning, ETL processing, dimensional modeling, SQL analytics, and business performance reporting.

> **Dataset note:** This project uses synthetic data generated for demonstration and portfolio purposes. It does not contain actual Eastman Chemical Company data or confidential business information.

## Project Overview

The platform helps analyze sales performance across products, customers, regions, categories, and sales channels. It converts raw datasets into clean analytical tables, loads them into PostgreSQL, and presents business metrics through Power BI reports.

### Key Features

- Automated synthetic data generation.
- Data cleaning and preparation using Python and Pandas.
- ETL pipeline for loading cleaned datasets into PostgreSQL.
- Star-schema data warehouse with fact and dimension tables.
- SQL queries for sales, revenue, profit, and product performance analysis.
- Interactive Power BI dashboards with KPIs, charts, tables, and slicers.
- Data validation through SQL queries and reconciliation with dashboard metrics.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data generation and ETL |
| Pandas | Data cleaning and transformation |
| PostgreSQL | Data warehouse and analytical queries |
| SQL | Schema design, data validation, and analytics |
| Power BI Desktop | Interactive dashboards and reporting |
| Git and GitHub | Version control and project documentation |
| VS Code | Development environment |

## Project Architecture

```text
Synthetic Data Generation
          |
          v
     Raw CSV Files
          |
          v
 Data Cleaning with Python
          |
          v
   Cleaned CSV Files
          |
          v
 PostgreSQL Staging Tables
          |
          v
  Star-Schema Data Warehouse
          |
          v
   SQL Analytics and DAX
          |
          v
   Power BI Dashboards
          |
          v
 Business Insights and Reporting
```

## Dataset Overview

The project contains the following synthetic datasets:

| Dataset | Records |
|---|---:|
| Customers | 2,000 |
| Products | 100 |
| Orders | 50,000 |
| Returns | 1,954 |

The raw customer data includes data-quality issues such as missing industry values, inconsistent region labels, and duplicate records. The cleaning pipeline prepares the data for analytical use.

The generated dataset covers January 2024 through September 2026.

## Repository Structure

```text
Business-Intelligence-Sales-Analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   └── Screenshots/
│       ├── Screenshot-1.png
│       ├── Screenshot-2.png
│       └── ...
│
├── etl/
│   ├── generate_data.py
│   ├── create_data_issues.py
│   ├── clean_data.py
│   └── load_data.py
│
├── notebooks/
│
├── powerbi/
│   ├── sales_analytics.pbix
│   └── BI_HACKATHON.pbix
│
├── sql/
│   ├── schema.sql
│   └── analytics.sql
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

**Note:** The `.env` file contains local configuration and should not be committed to GitHub. Raw and processed CSV files are excluded from version control; generate them locally by following the setup instructions.

## ETL Pipeline

The pipeline is organized into four Python scripts.

### 1. Data Generation

**File:** `etl/generate_data.py`

Generates synthetic customers, products, orders, and returns for the analytics workflow.

### 2. Data Quality Issue Creation

**File:** `etl/create_data_issues.py`

Introduces selected data-quality issues into the generated datasets to simulate common problems encountered in real-world data pipelines.

### 3. Data Cleaning

**File:** `etl/clean_data.py`

Cleans the raw datasets by addressing issues such as duplicate customer records, missing values, inconsistent categories or regions, and invalid order records.

The current cleaning run produced:

- 2,000 customers
- 100 products
- 50,000 orders
- 1,954 returns

The cleaned datasets are saved under `data/processed/`.

### 4. PostgreSQL Loading

**File:** `etl/load_data.py`

Loads the cleaned datasets into PostgreSQL staging tables for subsequent warehouse processing and analytics.

The successful staging load reported:

- 2,000 customers loaded
- 100 products loaded
- 50,000 orders loaded

## Data Warehouse Design

The project uses a star-schema model to support analytical queries and Power BI reporting.

### Dimension Tables

| Table | Purpose |
|---|---|
| `dim_customer` | Customer attributes |
| `dim_product` | Product and category attributes |
| `dim_date` | Date-related attributes |
| `dim_sales_channel` | Sales channel attributes |

### Fact Table

| Table | Purpose |
|---|---|
| `fact_sales` | Sales transactions and associated measures |

The `fact_sales` table connects to the four dimensions through foreign-key relationships:

- `customer_key` → `dim_customer`
- `product_key` → `dim_product`
- `date_key` → `dim_date`
- `channel_key` → `dim_sales_channel`

This structure supports analysis across multiple business dimensions while keeping transaction-level measures in the fact table.

## Power BI Dashboards

The Power BI report contains two analytical pages.

### 1. Executive Overview

Provides a high-level view of sales performance.

**Key performance indicators:**
- Total Revenue
- Total Profit
- Profit Margin
- Total Orders
- Total Customers
- Average Order Value

**Visualizations:**
- Monthly Revenue Trend
- Revenue by Region
- Revenue by Product Category

**Filters:**
- Year
- Category
- Region

![Executive Overview Dashboard](docs/Screenshots/Screenshot-1.png)

### 2. Product Analytics

Focuses on product-level revenue and profitability.

**Visualizations:**
- Top 10 Products by Revenue
- Revenue by Product Category
- Top 10 Products by Profit
- Product-level detail table

**Filters:**
- Category
- Year

The product table includes attributes such as product name, category, subcategory, unit price, unit cost, total revenue, and total profit.

![Product Analytics Dashboard](docs/Screenshots/Screenshot-2.png)

## SQL Analytics

**File:** `sql/analytics.sql`

The SQL analysis supports business questions such as:

- What is the total revenue and profit?
- What is the overall profit margin?
- Which regions generate the most revenue?
- Which products contribute the most revenue?
- How does revenue vary by product category?
- How does revenue change over time?
- How do sales channels compare?

The queries can be extended with common table expressions, window functions, year-over-year growth, customer segmentation, and additional profitability analysis.

## DAX Measures

The Power BI report uses DAX measures to calculate business KPIs.

```dax
Total Revenue =
SUM('public fact_sales'[revenue])
```

```dax
Total Cost =
SUM('public fact_sales'[cost])
```

```dax
Total Profit =
SUM('public fact_sales'[profit])
```

```dax
Profit Margin =
DIVIDE([Total Profit], [Total Revenue], 0)
```

```dax
Total Orders =
DISTINCTCOUNT('public fact_sales'[order_id])
```

```dax
Average Order Value =
DIVIDE([Total Revenue], [Total Orders], 0)
```

```dax
Total Customers =
DISTINCTCOUNT('public dim_customer'[customer_id])
```

These measures power the KPI cards and respond to report filters.

## Data Validation

The PostgreSQL validation query returned the following results for the synthetic sales dataset:

| Metric | Result |
|---|---:|
| Total sales rows | 50,000 |
| Distinct orders | 50,000 |
| Total Revenue | 8,861,619,904.35 |
| Total Profit | 2,423,578,378.12 |
| Profit Margin | 27.35% |

The database checks also confirmed the presence of the five expected warehouse tables and the four foreign-key relationships connecting `fact_sales` to its dimensions.

These values describe the generated project dataset. They are not actual company financial results.

## Getting Started

### Prerequisites

Install the following software:

- Python 3.12 or another compatible Python version.
- PostgreSQL.
- A PostgreSQL client such as pgAdmin 4.
- Power BI Desktop.
- Git (optional, for cloning the repository).

### 1. Clone the Repository

```bash
git clone https://github.com/Nihal-agarwal-10/business-intelligence-sales-analytics.git
cd business-intelligence-sales-analytics
```

Alternatively, download the repository as a ZIP file and extract it.

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If Python 3.12 is not installed, use a compatible Python version available on your system.

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Generate the Data

Run the scripts in the following order:

```powershell
python etl/generate_data.py
python etl/create_data_issues.py
python etl/clean_data.py
```

This generates the local CSV files, introduces selected data-quality issues, and produces cleaned datasets.

### 5. Configure PostgreSQL

1. Start your PostgreSQL server.
2. Create a database named `sales_analytics`.
3. Configure the database connection settings required by `etl/load_data.py` in your local environment.
4. Keep database credentials out of source control.

The exact connection variable names and configuration format must match those implemented in the Python loading script.

### 6. Load the Data

```powershell
python etl/load_data.py
```

Check the terminal output for confirmation that the staging data has loaded successfully.

### 7. Create and Populate the Warehouse

Use `sql/schema.sql` to inspect and execute the warehouse schema setup. Ensure that the dimension and fact tables are created and populated according to the script's implementation.

Run the relevant SQL validation and analytical queries in `sql/analytics.sql` using pgAdmin or another PostgreSQL client.

### 8. Open the Power BI Report

1. Open `powerbi/sales_analytics.pbix` in Power BI Desktop.
2. Configure the PostgreSQL connection for your local environment if prompted.
3. Refresh the data.
4. Verify that the report visuals and slicers display the expected metrics.

**Important:** The setup steps assume that the schema and loading scripts are consistent with the described staging-to-warehouse workflow. If your local scripts implement a different execution sequence, follow the actual SQL and Python code.

## Limitations

- The datasets are synthetic and do not represent a real company's operations.
- Raw and processed data files are generated locally rather than stored in the repository.
- Database credentials and local connection settings are not included.
- The report depends on a correctly configured PostgreSQL database.
- The current project focuses on descriptive analytics and BI reporting rather than predictive machine learning.

## Future Improvements

Potential extensions include:

- Add automated data-quality checks and pipeline logging.
- Introduce incremental loading and duplicate-load protection.
- Add year-over-year revenue and profit analysis.
- Expand customer retention and repeat-purchase analysis.
- Analyze returns and their impact on profitability.
- Add automated testing for ETL transformations and SQL metrics.
- Improve deployment and refresh automation.

## Author

**Nihal Agarwal**

B.Tech — Computer Science and Business Systems

GITAM University, Hyderabad

GitHub: [Nihal-agarwal-10](https://github.com/Nihal-agarwal-10)

---

*Built as a portfolio project demonstrating practical skills in Python, SQL, PostgreSQL, ETL, dimensional modeling, and Power BI.*
