-- app/sql/avg_items_per_order.sql

WITH orders AS (
  SELECT transaction_id, gross_sales
  FROM detail_items
  WHERE transaction_id IS NOT NULL
)
SELECT
  COUNT(DISTINCT transaction_id) AS total_orders,
  COUNT(*) AS total_items,
  ROUND(SUM(gross_sales), 2) AS total_sales,
  ROUND(COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT transaction_id), 0), 2) AS avg_items_per_order,
  ROUND(SUM(gross_sales) / NULLIF(COUNT(DISTINCT transaction_id), 0), 2) AS avg_order_value
FROM orders;
