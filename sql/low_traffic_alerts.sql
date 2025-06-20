-- app/sql/low_traffic_alerts.sql

WITH daily AS (
  SELECT
    date,
    COUNT(DISTINCT transaction_id) AS orders,
    ROUND(SUM(gross_sales), 2) AS total_sales
  FROM detail_items
  WHERE date IS NOT NULL
  GROUP BY date
),
avg_stats AS (
  SELECT
    ROUND(AVG(orders), 2) AS avg_orders,
    ROUND(STDDEV(orders), 2) AS std_orders
  FROM daily
)
SELECT
  d.date,
  d.orders,
  d.total_sales,
  a.avg_orders,
  a.std_orders,
  CASE
    WHEN d.orders < a.avg_orders - a.std_orders THEN '🔻 BELOW AVERAGE'
    ELSE 'Normal'
  END AS traffic_flag
FROM daily d, avg_stats a
ORDER BY d.date DESC;
