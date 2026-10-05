# Architecture

Medallion pipeline on Databricks (Delta tables in `steam_data.default`).

```
raw CSV (Volume)
  steam_games.csv, steam_games_reviews.csv
        |
        v
BRONZE   steam_games, review                     (raw, as loaded)
        |
        v
SILVER   silver_games                            (deduped, typed, price <= 1000, owners = midpoint)
         game_genres      (app_id, genre)        (many-to-many, 10 real genres only)
         game_categories  (app_id, category)     (many-to-many)
        |
        v
GOLD     gold_games                              (dates, price bands, review ratio, genre_count)
```

## Key decisions
- Genres and categories are split into their own tables, since a game can have several.
- Genres like Early Access or Free to Play are not game genres. A game is dropped only if none of its genres is in the list of 10 real genres.
- `aventure` / `aventura` are fixed to `Adventure`.
- Prices above 1000 are dropped (Steam's most expensive game is about 1000).
- Median playtime is used instead of the mean because the data is right-skewed.

## Limitation
Playtime analysis only covers games with recorded playtime (about 9%), which are likely more established titles.
