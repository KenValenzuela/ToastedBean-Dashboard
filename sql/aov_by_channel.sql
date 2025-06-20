-- sql/aov_by_channel.sql
SELECT
  channel,
  COUNT(*) AS order_count,
  ROUND(SUM(gross_sales), 2) AS total_revenue,
  ROUND(SUM(gross_sales)/COUNT(*), 2) AS avg_order_value
FROM detail_items
GROUP BY channel
ORDER BY total_revenue DESC;
