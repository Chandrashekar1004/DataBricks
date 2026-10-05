SELECT genre, COUNT(*) AS count
FROM steam_data.default.game_genres
GROUP BY genre
ORDER BY count DESC;
