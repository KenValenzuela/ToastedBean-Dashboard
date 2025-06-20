-- app/sql/customer_frequency.sql

SELECT
  customer_id,
  COUNT(DISTINCT date) AS active_days,
  COUNT(*) AS total_visits,
  ROUND(SUM(gross_sales), 2) AS total_spent
FROM detail_items
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY total_visits DESC
LIMIT 20;
