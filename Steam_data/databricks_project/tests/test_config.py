from src.utils.config_loader import load_config, raw_path, table_name


def test_table_name():
    cfg = load_config()
    assert table_name(cfg, "silver_games") == "steam_data.default.silver_games"


def test_raw_path():
    cfg = load_config()
    assert raw_path(cfg, "games_file").endswith("/steam_games.csv")


def test_all_pipeline_tables_defined():
    cfg = load_config()
    for key in ["bronze_games", "bronze_reviews", "silver_games", "game_genres", "game_categories", "gold_games"]:
        assert key in cfg["tables"]
