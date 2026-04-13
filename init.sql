CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES
    ('Alice Silva', 'alice@example.com'),
    ('Bruno Costa', 'bruno@example.com'),
    ('Carla Mendes', 'carla@example.com');
