CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(8) NOT NULL,
    password VARCHAR(15) NOT NULL,
    email VARCHAR(255) NOT NULL
);
