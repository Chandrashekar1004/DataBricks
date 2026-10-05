CREATE OR REPLACE TABLE steam_data.default.gold_games AS

WITH genre_counts AS (
    SELECT
        app_id,
        COUNT(DISTINCT genre) AS genre_count
    FROM steam_data.default.game_genres
    GROUP BY app_id
)

SELECT
    g.app_id,
    g.name,

    -- Release date information
    TO_DATE(g.release_date, 'yyyy-MM-dd') AS release_date,
    YEAR(TO_DATE(g.release_date, 'yyyy-MM-dd')) AS release_year,
    MONTH(TO_DATE(g.release_date, 'yyyy-MM-dd')) AS release_month,
    DATE_FORMAT(
        TO_DATE(g.release_date, 'yyyy-MM-dd'),
        'MMMM'
    ) AS release_month_name,
    DATE_FORMAT(
        TO_DATE(g.release_date, 'yyyy-MM-dd'),
        'yyyy-MM'
    ) AS release_year_month,

    -- Price information
    g.price,
    g.price = 0 AS is_free,

    CASE
        WHEN g.price IS NULL THEN 'Unknown'
        WHEN g.price = 0     THEN '1. Free'
        WHEN g.price < 10    THEN '2. Under 10'
        WHEN g.price < 20    THEN '3. 10 to 20'
        WHEN g.price < 40    THEN '4. 20 to 40'
        ELSE                      '5. 40+'
    END AS price_band,

    -- Ownership and review information
    g.estimated_owners,
    g.positive,
    g.negative,

    g.positive + g.negative AS total_reviews,

    CASE
        WHEN g.positive + g.negative > 0
        THEN g.positive / (g.positive + g.negative)
    END AS positive_ratio,

    -- Engagement
    g.peak_ccu,
    g.median_playtime_forever,

    -- Review score
    CASE
        WHEN g.metacritic_score > 0
        THEN g.metacritic_score
    END AS metacritic_score,

    -- Platform availability
    g.windows,
    g.mac,
    g.linux,

    -- Genre information
    COALESCE(gc.genre_count, 0) AS genre_count

FROM steam_data.default.silver_games g

LEFT JOIN genre_counts gc
    ON g.app_id = gc.app_id;
