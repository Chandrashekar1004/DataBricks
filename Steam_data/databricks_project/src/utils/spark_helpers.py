"""Small Spark helpers shared by the Bronze, Silver and Gold steps."""
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

SQL_DIR = Path(__file__).resolve().parents[2] / "sql"

# The .sql files use this namespace so they can also be run on their own.
SQL_DEFAULT_NAMESPACE = "steam_data.default"


def get_spark() -> SparkSession:
    return SparkSession.builder.getOrCreate()


def table_size(spark, df, name):
    """Show rows and columns of a DataFrame."""
    data = [(name, df.count(), len(df.columns))]
    spark.createDataFrame(data, ["Table", "Rows", "Cols"]).show()


def null_counts(spark, df):
    """Return a DataFrame with the number of nulls per column."""
    counts = {c: df.filter(col(c).isNull()).count() for c in df.columns}
    return spark.createDataFrame(counts.items(), ["column", "null_count"])


def run_sql_file(spark, relative_path: str, cfg: dict = None):
    """
    Run every statement in a file under sql/ (statements are separated by ';').
    If cfg is given, steam_data.default in the SQL is replaced by cfg catalog.schema.
    """
    text = (SQL_DIR / relative_path).read_text()
    if cfg:
        text = text.replace(SQL_DEFAULT_NAMESPACE, f"{cfg['catalog']}.{cfg['schema']}")
    for statement in (s.strip() for s in text.split(";")):
        if statement:
            spark.sql(statement)
