```sql
PRAGMA foreign_keys = ON;

-- =========================
-- TABLE CREATION
-- =========================

CREATE TABLE Products (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    entry_date TEXT NOT NULL,
    brand TEXT,
    stock_available INTEGER NOT NULL CHECK (stock_available >= 0)
);

CREATE TABLE Invoices (
    invoice_number INTEGER PRIMARY KEY AUTOINCREMENT,
    purchase_date TEXT NOT NULL,
    buyer_email TEXT NOT NULL,
    total_amount REAL NOT NULL CHECK (total_amount >= 0)
);

CREATE TABLE Invoice_Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number INTEGER NOT NULL,
    product_code TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    total_amount REAL NOT NULL CHECK (total_amount >= 0),

    FOREIGN KEY (invoice_number)
        REFERENCES Invoices(invoice_number),

    FOREIGN KEY (product_code)
        REFERENCES Products(code)
);

CREATE TABLE Shopping_Carts (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_email TEXT NOT NULL
);

CREATE TABLE Shopping_Cart_Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    product_code TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),

    FOREIGN KEY (cart_id)
        REFERENCES Shopping_Carts(cart_id),

    FOREIGN KEY (product_code)
        REFERENCES Products(code)
);

-- =========================
-- ALTER TABLE
-- =========================

ALTER TABLE Invoices
ADD COLUMN buyer_phone TEXT;

ALTER TABLE Invoices
ADD COLUMN cashier_employee_code TEXT;

-- =========================
-- SAMPLE DATA
-- =========================

INSERT INTO Products
(code, name, price, entry_date, brand, stock_available)
VALUES
('P001', 'Laptop', 350000, '2025-06-17', 'Lenovo', 10),
('P002', 'Mouse', 15000, '2025-06-17', 'Logitech', 50),
('P003', 'Monitor', 120000, '2025-06-17', 'Samsung', 20),
('P004', 'Keyboard', 55000, '2025-06-17', 'Redragon', 30);

INSERT INTO Invoices
(
    purchase_date,
    buyer_email,
    total_amount,
    buyer_phone,
    cashier_employee_code
)
VALUES
('2025-06-17', 'ana@email.com', 405000, '8888-1111', 'EMP001'),
('2025-06-17', 'ana@email.com', 120000, '8888-1111', 'EMP002'),
('2025-06-17', 'carlos@email.com', 70000, '8999-2222', 'EMP001');

INSERT INTO Invoice_Products
(invoice_number, product_code, quantity, total_amount)
VALUES
(1, 'P001', 1, 350000),
(1, 'P004', 1, 55000),
(2, 'P003', 1, 120000),
(3, 'P002', 1, 15000),
(3, 'P004', 1, 55000);

-- =========================
-- REQUIRED QUERIES
-- =========================

-- 1. Get all stored products
SELECT *
FROM Products;

-- 2. Get all products with a price greater than 50000
SELECT *
FROM Products
WHERE price > 50000;

-- 3. Get all purchases of a specific product by product code
SELECT *
FROM Invoice_Products
WHERE product_code = 'P004';

-- 4. Get all purchases grouped by product
-- showing the total quantity purchased
SELECT
    product_code,
    SUM(quantity) AS total_purchased
FROM Invoice_Products
GROUP BY product_code;

-- 5. Get all invoices made by the same buyer
SELECT *
FROM Invoices
WHERE buyer_email = 'ana@email.com';

-- 6. Get all invoices ordered by total amount descending
SELECT *
FROM Invoices
ORDER BY total_amount DESC;

-- 7. Get a single invoice by invoice number
SELECT *
FROM Invoices
WHERE invoice_number = 1;
```
