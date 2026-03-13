CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album TEXT,
    artist TEXT,
    review TEXT,
    review_points INTEGER,
    user_id INTEGER
);
