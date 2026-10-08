"""Run the whole pipeline (or one layer) from a job or a notebook."""
import sys

from src.ingestion.bronze_ingestion import run_bronze
from src.transformation.gold_transformation import run_gold
from src.transformation.silver_transformation import run_silver
from src.utils.config_loader import load_config
from src.utils.spark_helpers import get_spark

LAYERS = {"bronze": run_bronze, "silver": run_silver, "gold": run_gold}


def main(layers=("bronze", "silver", "gold")):
    spark = get_spark()
    cfg = load_config()
    for layer in layers:
        print(f"Running {layer} ...")
        LAYERS[layer](spark, cfg)


if __name__ == "__main__":
    # python -m src.pipeline            -> all layers
    # python -m src.pipeline silver     -> only silver
    main(tuple(sys.argv[1:]) or ("bronze", "silver", "gold"))
