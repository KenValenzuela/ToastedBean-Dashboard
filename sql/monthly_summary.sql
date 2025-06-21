-- sql/monthly_summary.sql
-- Monthly aggregates for use in trend dashboards

SELECT
  DATE_TRUNC('month', date) AS month,
  COUNT(DISTINCT transaction_id) AS total_orders,
  ROUND(SUM(gross_sales), 2) AS total_revenue,
  ROUND(AVG(gross_sales), 2) AS avg_order_value
FROM detail_items
GROUP BY month
ORDER BY month DESC;
