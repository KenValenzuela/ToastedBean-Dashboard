-- app/sql/hourly_volume_heatmap.sql

SELECT
  TO_CHAR(date, 'Day') AS weekday,
  EXTRACT(HOUR FROM datetime)::INT AS hour,
  COUNT(DISTINCT transaction_id) AS orders,
  ROUND(SUM(gross_sales), 2) AS revenue
FROM detail_items
WHERE datetime IS NOT NULL
GROUP BY weekday, hour
ORDER BY weekday, hour;
