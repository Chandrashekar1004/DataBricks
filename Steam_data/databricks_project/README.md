# Steam Games Databricks Project

Medallion pipeline (Bronze, Silver, Gold) on Steam games and reviews data, built with PySpark and Delta tables.

## Structure

```
databricks_project/
├── README.md
├── requirements.txt
├── config/config.yml          # catalog, schema, paths, table names
├── src/
│   ├── ingestion/             # bronze_ingestion.py
│   ├── transformation/        # silver_transformation.py, gold_transformation.py
│   ├── utils/                 # config_loader.py, spark_helpers.py
│   └── pipeline.py            # run all layers or one layer
├── notebooks/
│   ├── bronze/Bronze.ipynb
│   ├── silver/Silver_New.ipynb
│   └── gold/Gold.ipynb
├── sql/
│   ├── silver/                # 01-06 cleanup steps, run in order
│   ├── gold/                  # 01-03 gold table build
│   └── analysis/              # exploration queries
├── workflows/steam_pipeline_job.yml   # Databricks Job: bronze -> silver -> gold
├── tests/
└── docs/architecture.md
```

## Notebooks, `src/` and `sql/`
The SQL logic lives in one place only: the numbered files in `sql/`.
- The notebooks keep all the original markdown, exploration and charts. Where a cell used to hold a
  `CREATE`, `UPDATE`, `DELETE` or `ALTER` statement, it now calls `run_sql_file(spark, "silver/01_filter_price.sql", cfg)`.
  Read-only queries (`select ...`) stay inline in the notebooks.
- `src/` runs the same SQL files in the same order, so the whole pipeline can run as a job without opening a notebook.
- To change a transformation, edit the `.sql` file once. The notebooks and the job both pick it up.

The first code cell of the Silver and Gold notebooks is a small setup cell that adds the project root to
`sys.path` and loads `config/config.yml`. Keep the notebooks inside `notebooks/<layer>/` so that path works.

## Run
Databricks: run the notebooks in order (Bronze, Silver_New, Gold) or deploy `workflows/steam_pipeline_job.yml`.

From a repo checkout:
```
python -m src.pipeline            # all layers
python -m src.pipeline silver     # one layer
```

Tests: `pytest`

## Tables
| Layer  | Table                                            |
|--------|--------------------------------------------------|
| Bronze | `steam_games`, `review`                          |
| Silver | `silver_games`, `game_genres`, `game_categories` |
| Gold   | `gold_games`                                     |
