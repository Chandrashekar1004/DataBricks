-- Mean is far above the median, which confirms a right skew, so the median is the better engagement metric.
SELECT
  COUNT(*) AS games,
  ROUND(AVG(median_playtime_forever)/60, 1) AS mean_hours,
  ROUND(PERCENTILE(median_playtime_forever, 0.5)/60, 1) AS median_hours,
  ROUND(PERCENTILE(median_playtime_forever, 0.25)/60, 1) AS p25_hours,
  ROUND(PERCENTILE(median_playtime_forever, 0.75)/60, 1) AS p75_hours,
  ROUND(PERCENTILE(median_playtime_forever, 0.95)/60, 1) AS p95_hours
FROM steam_data.default.gold_games
WHERE median_playtime_forever > 0;
