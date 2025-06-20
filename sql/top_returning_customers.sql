SELECT
  customer_id,
  customer_name,
  COUNT(DISTINCT date) AS visit_days,
  COUNT(*) AS total_visits,
  ROUND(SUM(gross_sales), 2) AS total_spent,
  ROUND(AVG(gross_sales), 2) AS avg_spent_per_visit
FROM detail_items
WHERE
  customer_id IS NOT NULL
  AND TRIM(customer_name) IS NOT NULL
  AND TRIM(customer_name) NOT IN ('', ',')
GROUP BY customer_id, customer_name
ORDER BY total_visits DESC
LIMIT 20;
