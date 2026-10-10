-- ==========================================
-- BUSINESS INTELLIGENCE SALES ANALYTICS
-- ==========================================


-- 1. Total Revenue
SELECT
    SUM(revenue) AS total_revenue
FROM fact_sales;


-- 2. Total Cost
SELECT
    SUM(cost) AS total_cost
FROM fact_sales;


-- 3. Total Profit
SELECT
    SUM(profit) AS total_profit
FROM fact_sales;


-- 4. Profit Margin
SELECT
    ROUND(
        SUM(profit) / NULLIF(SUM(revenue), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM fact_sales;


-- 5. Revenue by Region
SELECT
    c.region,
    SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.region
ORDER BY revenue DESC;


-- 6. Profit by Region
SELECT
    c.region,
    SUM(f.profit) AS profit
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.region
ORDER BY profit DESC;


-- 7. Top 10 Products by Revenue
SELECT
    p.product_name,
    SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 10;


-- 8. Revenue by Product Category
SELECT
    p.category,
    SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY revenue DESC;


-- 9. Monthly Revenue
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- 10. Revenue by Sales Channel
SELECT
    sc.sales_channel,
    SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_sales_channel sc
    ON f.channel_key = sc.channel_key
GROUP BY sc.sales_channel
ORDER BY revenue DESC;