-- sql/zero_value_orders.sql
-- Detect $0 orders which may indicate test scans or voids

SELECT
  transaction_id,
  employee_name,
  date,
  COUNT(*) AS item_count,
  ROUND(SUM(gross_sales), 2) AS total_revenue
FROM detail_items
GROUP BY transaction_id, employee_name, date
HAVING SUM(gross_sales) < 0.01
ORDER BY date DESC;
