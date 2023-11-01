CREATE TABLE food (
    food_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    food_name TEXT NOT NULL,
    protein INTEGER NOT NULL,
    carbohydrates INTEGER NOT NULL,
    fats INTEGER NOT NULL,
    calories INTEGER NOT NULL
);

CREATE TABLE date_id (
    date_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    entry_date INTEGER NOT NULL
);

CREATE TABLE dateid_foodid (
    date_id INTEGER NOT NULL,
    food_id INTEGER NOT NULL,
    PRIMARY KEY (date_id, food_id)
);