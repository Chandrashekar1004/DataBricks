-- Genres and categories now live in game_genres and game_categories, so drop them here.
ALTER TABLE steam_data.default.silver_games
DROP COLUMNS genres, categories;
