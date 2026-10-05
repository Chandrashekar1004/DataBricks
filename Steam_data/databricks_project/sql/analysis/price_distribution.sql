-- Most prices are below 100. Anything above 200 looks unusual but is not necessarily an anomaly.
SELECT price, COUNT(app_id) AS count
FROM steam_data.default.silver_games
GROUP BY price;
