-- Keep only real game genres in the genre table (drops Early Access, Free to Play, etc.)
DELETE FROM steam_data.default.game_genres
WHERE genre NOT IN (
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
);
