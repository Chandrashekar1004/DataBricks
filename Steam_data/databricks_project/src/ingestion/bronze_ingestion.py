"""Bronze layer: load the raw CSV files and save them as Delta tables."""
import pandas as pd

from src.utils.config_loader import raw_path, table_name


def read_reviews(spark, path: str):
    return (
        spark.read.format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .load(path)
    )


def read_games(spark, path: str, csv_options: dict):
    """The games CSV has bad rows, so it is read with pandas first and then converted."""
    pdf = pd.read_csv(
        path,
        encoding=csv_options["encoding"],
        on_bad_lines=csv_options["on_bad_lines"],
        engine=csv_options["engine"],
    )
    return spark.createDataFrame(pdf)


def write_delta(df, table: str):
    df.write.format("delta").mode("overwrite").saveAsTable(table)


def run_bronze(spark, cfg: dict):
    reviews = read_reviews(spark, raw_path(cfg, "reviews_file"))
    games = read_games(spark, raw_path(cfg, "games_file"), cfg["games_csv_options"])

    write_delta(games, table_name(cfg, "bronze_games"))
    write_delta(reviews, table_name(cfg, "bronze_reviews"))
