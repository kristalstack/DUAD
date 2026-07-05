DROP TABLE IF EXISTS bill_items;
DROP TABLE IF EXISTS bills;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users_app;

CREATE TABLE users_app (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    stock INT NOT NULL CHECK (stock >= 0)
);

CREATE TABLE bills (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users_app(id),
    total NUMERIC(10,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'Activa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bill_items (
    id SERIAL PRIMARY KEY,
    bill_id INT NOT NULL REFERENCES bills(id),
    product_id INT NOT NULL REFERENCES products(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2),
    subtotal NUMERIC(10,2)
);

INSERT INTO users_app (name, email)
VALUES
('Kristal Pastor', 'kristal@email.com'),
('Juan Pérez', 'juan@email.com');

INSERT INTO products (name, price, stock)
VALUES
('Laptop', 12000.00, 5),
('Mouse', 250.00, 20),
('Teclado', 600.00, 10);