-- 'aventure' and 'aventura' are spelling variants of Adventure
UPDATE steam_data.default.game_genres
SET genre = 'Adventure'
WHERE LOWER(genre) IN ('aventure', 'aventura');
