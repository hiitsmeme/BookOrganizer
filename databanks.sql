CREATE TABLE User(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    passwordhash CHAR(256) NOT NULL,
    total_books INT NOT NULL,
    total_pages INT NOT NULL
);

CREATE TABLE Books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, 
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    pages INT NOT NULL,
    rating INT NOT NULL,
    month INT NOT NULL,
    year INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User (id)
);