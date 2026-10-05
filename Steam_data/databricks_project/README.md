# Steam Games Databricks Project

Medallion pipeline (Bronze, Silver, Gold) on Steam games and reviews data, built with PySpark and Delta tables.

## Structure

```
databricks_project/
├── README.md
├── requirements.txt
├── config/config.yml          # catalog, schema, paths, table names
├── notebooks/
│   ├── bronze/Bronze.ipynb
│   ├── silver/Silver_New.ipynb
│   └── gold/Gold.ipynb
├── sql/
│   ├── silver/                # 01-06 cleanup steps, run in order
│   ├── gold/                  # 01-03 gold table build
│   └── analysis/              # exploration queries
└── docs/architecture.md
```

## Notebooks, `src/` and `sql/`
The SQL logic lives in one place only: the numbered files in `sql/`.
- The notebooks keep all the original markdown, exploration and charts. Where a cell used to hold a
  `CREATE`, `UPDATE`, `DELETE` or `ALTER` statement, it now calls `run_sql_file(spark, "silver/01_filter_price.sql", cfg)`.
  Read-only queries (`select ...`) stay inline in the notebooks.
that path works.

## Run
Databricks: run the notebooks in order (Bronze, Silver_New, Gold) o


## Tables
| Layer  | Table                                            |
|--------|--------------------------------------------------|
| Bronze | `steam_games`, `review`                          |
| Silver | `silver_games`, `game_genres`, `game_categories` |
| Gold   | `gold_games`                                     |
