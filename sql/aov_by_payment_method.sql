-- app/sql/aov_by_payment_method.sql

SELECT
  COALESCE(card_brand, 'Cash') AS payment_method,
  COUNT(DISTINCT transaction_id) AS total_orders,
  ROUND(SUM(gross_sales), 2) AS total_revenue,
  ROUND(SUM(gross_sales) / COUNT(DISTINCT transaction_id), 2) AS avg_order_value
FROM detail_items
WHERE transaction_id IS NOT NULL
GROUP BY payment_method
ORDER BY avg_order_value DESC;
