SELECT
    sales_type,
    date_range AS date,
    ROUND(SUM(amount), 2) AS total_amount
FROM
    sales_summary
GROUP BY
    sales_type, date_range
ORDER BY
    date DESC,
    sales_type;
