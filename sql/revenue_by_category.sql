-- sql/revenue_by_category.sql

SELECT
    category,
    CONCAT(TO_CHAR(start_date, 'MM/DD/YYYY'), '–', TO_CHAR(end_date, 'MM/DD/YYYY')) AS date_range,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM category_sales
WHERE category IS NOT NULL
GROUP BY category, start_date, end_date
ORDER BY start_date DESC, total_revenue DESC;
