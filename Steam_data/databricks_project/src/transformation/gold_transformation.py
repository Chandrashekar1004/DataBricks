"""Gold layer: build the analytics table and reusable analysis helpers."""
from pyspark.sql import functions as F

from src.utils.config_loader import table_name
from src.utils.spark_helpers import run_sql_file


def run_gold(spark, cfg: dict):
    run_sql_file(spark, "gold/01_create_gold_games.sql", cfg)
    run_sql_file(spark, "gold/02_enable_column_mapping.sql", cfg)
    run_sql_file(spark, "gold/03_drop_helper_columns.sql", cfg)


def genre_playtime_stats(games_with_genres, min_games: int = 30):
    """
    Playtime per genre (games with recorded playtime only).
    Reports the median of medians, the average of medians and the skew ratio between them.
    """
    return (
        games_with_genres.filter("median_playtime_forever > 0")
        .groupBy("genre")
        .agg(
            F.countDistinct("app_id").alias("num_games"),
            F.round(F.expr("percentile(median_playtime_forever, 0.5)") / 60, 1).alias("median_of_medians_hrs"),
            F.round(F.avg("median_playtime_forever") / 60, 1).alias("avg_of_medians_hrs"),
        )
        .withColumn("skew_ratio", F.round(F.col("avg_of_medians_hrs") / F.col("median_of_medians_hrs"), 2))
        .filter(f"num_games >= {min_games}")
        .orderBy(F.desc("median_of_medians_hrs"))
    )


def load_gold_with_genres(spark, cfg: dict):
    games = spark.table(table_name(cfg, "gold_games"))
    genres = spark.table(table_name(cfg, "game_genres"))
    return games.join(genres, on="app_id", how="inner")


def load_gold_with_categories(spark, cfg: dict):
    games = spark.table(table_name(cfg, "gold_games"))
    categories = spark.table(table_name(cfg, "game_categories"))
    return games.join(categories, on="app_id", how="inner")
