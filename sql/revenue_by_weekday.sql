-- app/sql/revenue_by_weekday.sql

SELECT
  TO_CHAR(date, 'Day') AS weekday,
  COUNT(*) AS orders,
  ROUND(SUM(gross_sales), 2) AS total_revenue,
  ROUND(AVG(gross_sales), 2) AS avg_order_value
FROM detail_items
WHERE date IS NOT NULL
GROUP BY weekday
ORDER BY total_revenue DESC;
