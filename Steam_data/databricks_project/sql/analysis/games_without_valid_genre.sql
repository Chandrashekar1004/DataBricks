-- Number of games that have no genre from our list of interested genres
SELECT COUNT(*) AS games_to_delete
FROM (
    SELECT app_id
    FROM steam_data.default.game_genres
    GROUP BY app_id
    HAVING SUM(
        CASE
            WHEN genre IN (
                'Action', 'Adventure', 'Casual', 'Indie', 'Massively Multiplayer',
                'RPG', 'Racing', 'Simulation', 'Sports', 'Strategy'
            )
            THEN 1
            ELSE 0
        END
    ) = 0
);
