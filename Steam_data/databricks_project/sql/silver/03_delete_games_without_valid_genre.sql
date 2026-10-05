-- Delete games that have no genre from our list of interested genres.
-- A game with several genres stays if at least one of them is in the list.
DELETE FROM steam_data.default.silver_games
WHERE app_id IN (
    SELECT app_id
    FROM steam_data.default.game_genres
    GROUP BY app_id
    HAVING SUM(
        CASE
            WHEN genre IN (
                'Action',
                'Adventure',
                'Casual',
                'Indie',
                'Massively Multiplayer',
                'RPG',
                'Racing',
                'Simulation',
                'Sports',
                'Strategy'
            )
            THEN 1
            ELSE 0
        END
    ) = 0
);
