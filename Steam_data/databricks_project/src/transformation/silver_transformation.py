"""Silver layer: clean the games table and split genres / categories into their own tables."""
from pyspark.sql.functions import col, explode, from_json, regexp_replace, split, trim
from pyspark.sql.types import ArrayType, StringType, StructField, StructType

from src.utils.config_loader import table_name
from src.utils.spark_helpers import run_sql_file

# genres / categories come in two formats: JSON objects [{"id":..,"description":..}] or plain lists
_OBJ_SCHEMA = ArrayType(
    StructType(
        [
            StructField("id", StringType(), True),
            StructField("description", StringType(), True),
        ]
    )
)
_STR_SCHEMA = ArrayType(StringType())


def select_game_columns(df, columns_to_keep):
    """Keep only the columns needed for the business problem and cast price to double."""
    return df.select(columns_to_keep).withColumn("price", col("price").cast("double"))


def parse_estimated_owners(df):
    """Turn a range like '20,000 - 50,000' into the midpoint of the range."""
    df = df.withColumn("estimated_owners", split(col("estimated_owners"), r"\.\.|\s*-\s*"))
    return df.withColumn(
        "estimated_owners",
        (
            regexp_replace(trim(col("estimated_owners").getItem(0)), ",", "").cast("double")
            + regexp_replace(trim(col("estimated_owners").getItem(1)), ",", "").cast("double")
        )
        / 2,
    )


def explode_json_or_list(df, source_col: str, out_col: str):
    """
    Build a (app_id, out_col) table from a column that is either JSON objects or a plain list.
    Used for both genres and categories (many-to-many with the game).
    """
    parsed_col = f"{source_col}_parsed"
    is_json = col(source_col).contains('"id"')

    json_rows = df.filter(is_json).withColumn(parsed_col, from_json(col(source_col), _OBJ_SCHEMA))
    str_rows = df.filter(~is_json).withColumn(parsed_col, from_json(col(source_col), _STR_SCHEMA))

    # JSON format: the name is in "description"
    from_objects = json_rows.select("app_id", explode(col(parsed_col)).alias("g")).select(
        "app_id", trim(col("g.description")).alias(out_col)
    )

    # Plain list format: the element already is the name
    from_strings = str_rows.select("app_id", explode(col(parsed_col)).alias(out_col)).withColumn(
        out_col, trim(col(out_col))
    )

    return (
        from_objects.unionByName(from_strings)
        .filter(col(out_col).isNotNull() & (col(out_col) != ""))
        .distinct()
    )


def _write_delta(df, table: str):
    (
        df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table)
    )


def run_silver(spark, cfg: dict):
    # 1. Clean the bronze games table
    games = spark.table(table_name(cfg, "bronze_games")).dropDuplicates()
    games = select_game_columns(games, cfg["silver"]["columns_to_keep"])
    games = parse_estimated_owners(games)
    _write_delta(games, table_name(cfg, "silver_games"))

    # 2. Drop prices above 1000
    run_sql_file(spark, "silver/01_filter_price.sql", cfg)

    # 3. Genres: own table, fix spelling, keep only real game genres
    silver_games = spark.table(table_name(cfg, "silver_games"))
    _write_delta(
        explode_json_or_list(silver_games, "genres", "genre"),
        table_name(cfg, "game_genres"),
    )
    run_sql_file(spark, "silver/02_fix_genre_spelling.sql", cfg)
    run_sql_file(spark, "silver/03_delete_games_without_valid_genre.sql", cfg)
    run_sql_file(spark, "silver/04_delete_invalid_genres.sql", cfg)

    # 4. Categories: own table
    silver_games = spark.table(table_name(cfg, "silver_games"))
    _write_delta(
        explode_json_or_list(silver_games, "categories", "category"),
        table_name(cfg, "game_categories"),
    )

    # 5. Genres and categories now live in their own tables, so drop them from silver_games
    run_sql_file(spark, "silver/05_enable_column_mapping.sql", cfg)
    run_sql_file(spark, "silver/06_drop_genre_category_columns.sql", cfg)
