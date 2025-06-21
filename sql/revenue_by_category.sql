-- sql/revenue_by_category.sql

SELECT
    DATE_TRUNC('month', start_date)::date AS month,
    category,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM category_sales
WHERE category IS NOT NULL
GROUP BY month, category
ORDER BY month DESC, total_revenue DESC;
