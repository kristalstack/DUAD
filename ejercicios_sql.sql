PRAGMA foreign_keys = ON;

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