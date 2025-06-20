-- app/sql/modifier_lift.sql

WITH exploded AS (
  SELECT
    unnest(string_to_array(modifiers_applied, ', ')) AS modifier,
    gross_sales
  FROM detail_items
  WHERE modifiers_applied IS NOT NULL
)
SELECT
  modifier,
  COUNT(*) AS usage_count,
  ROUND(AVG(gross_sales), 2) AS avg_gross_sales,
  ROUND(SUM(gross_sales), 2) AS total_sales
FROM exploded
GROUP BY modifier
ORDER BY avg_gross_sales DESC
LIMIT 15;
