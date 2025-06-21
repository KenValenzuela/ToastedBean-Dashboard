-- sql/revenue_by_category.sql
-- Cleaned to support DATE type and monthly aggregation

SELECT
  category,
  DATE_TRUNC('month', date) AS month,
  ROUND(SUM(revenue), 2) AS total_revenue
FROM category_sales
WHERE category IS NOT NULL
GROUP BY category, DATE_TRUNC('month', date)
ORDER BY month DESC, total_revenue DESC;
