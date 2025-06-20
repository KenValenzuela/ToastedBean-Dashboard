-- sql/daily_revenue.sql
SELECT
  date,
  ROUND(SUM(gross_sales), 2) AS total_revenue
FROM detail_items
GROUP BY date
ORDER BY date;
