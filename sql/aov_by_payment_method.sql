-- sql/aov_by_payment_method.sql
SELECT
  COALESCE(card_brand, 'Cash') AS payment_method,
  COUNT(DISTINCT transaction_id) AS order_count,
  ROUND(SUM(gross_sales), 2) AS total_revenue,
  CASE
    WHEN COUNT(DISTINCT transaction_id) > 0 THEN
      ROUND(SUM(gross_sales) / COUNT(DISTINCT transaction_id), 2)
    ELSE 0
  END AS avg_order_value
FROM detail_items
WHERE card_brand IS NOT NULL AND gross_sales > 0
GROUP BY payment_method
ORDER BY avg_order_value DESC;
