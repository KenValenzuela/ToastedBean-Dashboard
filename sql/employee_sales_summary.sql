-- sql/employee_sales_summary.sql
-- Summarize revenue by employee to detect test scans or top performers

SELECT
  employee_name,
  COUNT(DISTINCT transaction_id) AS order_count,
  ROUND(SUM(gross_sales), 2) AS total_revenue,
  ROUND(AVG(gross_sales), 2) AS avg_per_order
FROM detail_items
WHERE
  employee_name IS NOT NULL
  AND date >= date_trunc('month', CURRENT_DATE)
GROUP BY employee_name
ORDER BY total_revenue DESC;
