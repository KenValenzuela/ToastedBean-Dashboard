SELECT
    date_range AS date,
    ROUND(SUM(amount), 2) AS total_amount
FROM sales_summary
WHERE
    sales_type = 'Sale' AND
    amount > 0 AND
    TO_DATE(date_range, 'MM/DD/YYYY') >= date_trunc('month', CURRENT_DATE)
GROUP BY date_range
ORDER BY TO_DATE(date_range, 'MM/DD/YYYY');
