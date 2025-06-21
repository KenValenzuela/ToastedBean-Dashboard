-- sql/sales_trends.sql

SELECT
    CONCAT(TO_CHAR(start_date, 'MM/DD/YYYY'), '–', TO_CHAR(end_date, 'MM/DD/YYYY')) AS date_range,
    ROUND(SUM(amount), 2) AS total_amount
FROM sales_summary
WHERE sales_type = 'Sale'
GROUP BY start_date, end_date
ORDER BY start_date;
