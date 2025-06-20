-- sql/peak_hours.sql
SELECT
  EXTRACT(HOUR FROM time)::int AS hour,
  ROUND(SUM(gross_sales), 2) AS total_revenue,
  COUNT(*) AS order_count
FROM detail_items
GROUP BY hour
ORDER BY hour;
