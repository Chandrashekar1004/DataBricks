-- Delta tables don't support dropping columns unless column mapping is turned on.
ALTER TABLE steam_data.default.gold_games
SET TBLPROPERTIES ('delta.columnMapping.mode' = 'name');
