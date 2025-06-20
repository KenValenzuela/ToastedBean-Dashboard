-- sql/revenue_by_category.sql

SELECT
    category,
    date_range,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM
    category_sales
GROUP BY
    category, date_range
ORDER BY
    date_range DESC,
    total_revenue DESC;
