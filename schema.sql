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

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    album TEXT,
    value TEXT
);

CREATE TABLE item_classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    album TEXT,
    value TEXT
);

CREATE TABLE bids (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    comment_review INTEGER
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    image BLOB
);
