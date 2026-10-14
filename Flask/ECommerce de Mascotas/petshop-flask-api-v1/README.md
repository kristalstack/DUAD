# PetShop API 🐾

Backend API for managing users, products, shopping carts, sales, invoices, and returns for a pet-products e-commerce store.

## Technologies

* Python 3.11+
* Flask and Flask-SQLAlchemy
* PostgreSQL
* JWT authentication with PyJWT
* Redis through Flask-Caching
* Pytest and pytest-cov

## Getting Started

### Prerequisites

Make sure the following tools are installed and running:

* Python 3.11 or newer
* PostgreSQL
* Redis

### 1. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install the dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Create the PostgreSQL database

Create a separate database for the project:

```bash
createdb -U postgres petshop_db
```

If `createdb` is not directly available on macOS, use the path where PostgreSQL is installed. For example:

```bash
/Library/PostgreSQL/17/bin/createdb -h localhost -p 5432 -U postgres petshop_db
```

The command will request the PostgreSQL password.

### 4. Configure the environment variables

Copy the example configuration:

```bash
cp .env.example .env
```

Open `.env` and configure the PostgreSQL and Redis credentials:

```env
FLASK_ENV=development

SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
JWT_EXPIRES_MINUTES=60

DATABASE_URL=postgresql+psycopg2://postgres:your_postgres_password@localhost:5432/petshop_db

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_USERNAME=your_redis_username
REDIS_PASSWORD=your_redis_password
```

Generate a secure value for each secret key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Run the command twice and use a different generated value for `SECRET_KEY` and `JWT_SECRET_KEY`.

The `.env` file contains private credentials and must not be committed to the repository.

### 5. Create the database tables

Create all tables through SQLAlchemy:

```bash
flask --app run.py init-db
```

Expected result:

```text
Database initialized.
```

No manual SQL scripts are required. The `init-db` command calls `SQLAlchemy.create_all()`, and all application database operations are performed through the ORM.

### 6. Create the initial administrator

```bash
flask --app run.py create-admin
```

The command will request the administrator's name, email address, and password.

### 7. Start the server

```bash
flask --app run.py run --debug
```

The API will be available at:

```text
http://127.0.0.1:5000/api
```

Use the health endpoint to confirm that the server is running:

```http
GET /api/health
```

Expected response:

```json
{
  "status": "ok"
}
```

## Authentication

Register a client with `POST /api/auth/register` or sign in with `POST /api/auth/login`. Both endpoints return a JWT access token.

Include the token in protected requests:

```http
Authorization: Bearer <token>
```

Registration example:

```json
{
  "name": "Ana Pérez",
  "email": "ana@example.com",
  "password": "a-secure-password"
}
```

Users created through the public registration endpoint always receive the `client` role. The `admin` role can be assigned through the `create-admin` command or by an existing administrator.

Use `POST /api/auth/logout` to revoke the current JWT before it expires.

## Main Purchase Flow

1. The client creates a billing address with `POST /api/users/{id}/addresses`.
2. The client creates a shopping cart with `POST /api/carts`.
3. The client adds or changes product quantities with `PUT /api/carts/{cart_id}/items/{product_id}`.
4. The client completes the purchase with `POST /api/carts/{cart_id}/checkout`:

```json
{
  "address_id": 1,
  "payment_method": "SINPE",
  "payment_reference": "SINPE-2026-0001"
}
```

5. The client retrieves the invoice with `GET /api/invoices/{number}`.
6. The client returns one or more purchased units with `POST /api/invoices/{number}/returns`:

```json
{
  "reason": "Unopened product",
  "items": [
    {
      "invoice_item_id": 1,
      "quantity": 1
    }
  ]
}
```

Completing a purchase reduces product stock. Completing a return restores the corresponding quantity.

## Endpoints

| Method and route                                         | Permission    | Purpose                                                   |
| -------------------------------------------------------- | ------------- | --------------------------------------------------------- |
| `POST /api/auth/register`                                | Public        | Register a client                                         |
| `POST /api/auth/login`                                   | Public        | Obtain a JWT                                              |
| `POST /api/auth/logout`                                  | Authenticated | Revoke the current JWT                                    |
| `GET /api/users`                                         | Admin         | List users                                                |
| `GET /api/users/{id}`                                    | Owner/Admin   | Retrieve a user                                           |
| `PATCH`, `DELETE /api/users/{id}`                        | Admin         | Update or deactivate a user                               |
| `GET`, `POST /api/users/{id}/addresses`                  | Owner/Admin   | List or create addresses                                  |
| `PATCH`, `DELETE /api/users/{id}/addresses/{address_id}` | Owner/Admin   | Update or delete an address                               |
| `GET /api/products`                                      | Authenticated | List products                                             |
| `GET /api/products/{id}`                                 | Authenticated | Retrieve a product                                        |
| `POST /api/products`                                     | Admin         | Create a product                                          |
| `PATCH`, `DELETE /api/products/{id}`                     | Admin         | Update or deactivate a product                            |
| `GET`, `POST /api/carts`                                 | Client/Admin  | List or create carts; administrators can list all carts   |
| `GET`, `DELETE /api/carts/{id}`                          | Owner/Admin   | Retrieve or delete an open cart                           |
| `PUT`, `DELETE /api/carts/{id}/items/{product_id}`       | Owner/Admin   | Set or remove a cart item                                 |
| `POST /api/carts/{id}/checkout`                          | Owner/Admin   | Convert a cart into a sale                                |
| `GET /api/invoices`                                      | Client/Admin  | List owned invoices; administrators can list all invoices |
| `GET /api/invoices/{number}`                             | Owner/Admin   | Retrieve an invoice                                       |
| `PATCH`, `DELETE /api/invoices/{number}`                 | Admin         | Change invoice status or delete an eligible invoice       |
| `POST /api/invoices/{number}/returns`                    | Owner/Admin   | Create a return and restore stock                         |

Deleting products and users performs a soft deletion to preserve historical records.

An invoice can only be deleted when it has been cancelled or fully refunded.

## Caching

The application uses Redis through Flask-Caching.

The following resources are cached:

* Product lists
* Individual product details
* Invoice lookups by invoice number

Product cache entries are invalidated when a product is created, updated, deactivated, sold, or returned.

Invoice cache entries are invalidated when an invoice status changes, a return is created, or an invoice is deleted.

The caches also use time-to-live values as an additional safeguard against stale data.

Shopping carts are not cached because they change frequently.

## Running the Tests

The automated tests use an in-memory SQLite database and a local cache. This keeps the tests isolated from the development PostgreSQL and Redis services.

On macOS or Linux:

```bash
chmod +x run_tests.sh
./run_tests.sh
```

The tests can also be executed directly:

```bash
python -m pytest
```

The test script saves a short report in:

```text
test-report.txt
```

The HTML coverage report is generated at:

```text
htmlcov/index.html
```

The test suite includes:

* Registration and login
* Duplicate email validation
* Incorrect credentials
* JWT revocation
* Authentication requirements
* Administrator permissions
* Product creation, update, and deactivation
* Duplicate SKU validation
* Product price and stock validation
* User ownership restrictions
* Cart management
* Stock validation during checkout
* Stock reduction after a purchase
* Stock restoration after a return
* Prevention of returns exceeding the purchased quantity

## Technical Documentation

See [`docs/technical-design.md`](docs/technical-design.md) for:

* The entity-relationship diagram
* Database normalization decisions
* Transaction and concurrency handling
* Authentication and authorization design
* Cache selection, TTL values, and invalidation conditions
* API design decisions
