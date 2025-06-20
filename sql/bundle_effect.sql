-- app/sql/bundle_effect.sql

WITH orders AS (
  SELECT
    transaction_id,
    COUNT(*) AS item_count,
    SUM(gross_sales) AS total_revenue
  FROM detail_items
  WHERE transaction_id IS NOT NULL
  GROUP BY transaction_id
)
SELECT
  item_count,
  COUNT(*) AS order_count,
  ROUND(AVG(total_revenue), 2) AS avg_order_value,
  ROUND(AVG(total_revenue) / item_count, 2) AS avg_value_per_item
FROM orders
GROUP BY item_count
HAVING item_count > 0
ORDER BY item_count;
