-- sql/sales_trends.sql

SELECT
    sales_type,
    date_range,
    ROUND(SUM(amount), 2) AS total_amount
FROM
    sales_summary
GROUP BY
    sales_type, date_range
ORDER BY
    date_range DESC,
    sales_type;
