-- Drop the rows where price is greater than 1000 as they are small in number.
-- Steam's most expensive game is about 1000 dollars, so anything above is treated as bad data.
CREATE OR REPLACE TABLE steam_data.default.silver_games AS
SELECT *
FROM steam_data.default.silver_games
WHERE price IS NULL OR price <= 1000;
