-- sql/top_items.sql

SELECT
    item,
    category,
    COUNT(*) AS sale_count,
    ROUND(SUM(gross_sales), 2) AS total_gross_sales
FROM
    detail_items
GROUP BY
    item, category
ORDER BY
    total_gross_sales DESC
LIMIT 25;
