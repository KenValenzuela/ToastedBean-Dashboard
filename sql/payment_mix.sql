-- sql/payment_mix.sql
SELECT
  COALESCE(card_brand, 'Cash') AS payment_method,
  COUNT(*) AS transaction_count,
  ROUND(SUM(gross_sales), 2) AS total_revenue
FROM detail_items
GROUP BY payment_method
ORDER BY total_revenue DESC;
