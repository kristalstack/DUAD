from flask import Flask, jsonify, request
from psycopg2 import DatabaseError, IntegrityError

from db import get_connection


app = Flask(__name__)


# ---------------------------------------------------------
# VALID VALUES
# ---------------------------------------------------------

VALID_USER_STATUSES = [
    "active",
    "inactive",
    "suspended",
]

VALID_CAR_STATUSES = [
    "available",
    "rented",
    "maintenance",
    "unavailable",
]

VALID_RENTAL_STATUSES = [
    "reserved",
    "active",
    "completed",
    "cancelled",
]

# Los estados iniciales se derivan de VALID_RENTAL_STATUSES.
INITIAL_RENTAL_STATUSES = VALID_RENTAL_STATUSES[:2]

RENTAL_STATUS_TRANSITIONS = {
    "reserved": ["active", "cancelled"],
    "active": ["completed", "cancelled"],
    "completed": [],
    "cancelled": [],
}


# ---------------------------------------------------------
# ALLOWED FILTERS
# ---------------------------------------------------------

USER_FILTER_COLUMNS = {
    "id",
    "full_name",
    "email",
    "username",
    "birth_date",
    "account_status",
    "is_delinquent",
}

CAR_FILTER_COLUMNS = {
    "id",
    "brand",
    "model",
    "manufacturing_year",
    "car_status",
}

RENTAL_FILTER_COLUMNS = {
    "id",
    "user_id",
    "car_id",
    "rental_date",
    "rental_status",
}


# ---------------------------------------------------------
# GENERAL ENDPOINTS
# ---------------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Lyfter Car Rental API"
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "OK"
    }), 200


@app.route("/database", methods=["GET"])
def database():
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT current_database() AS current_database;"
            )
            database_name = cursor.fetchone()

        return jsonify(database_name), 200

    except DatabaseError as error:
        return jsonify({
            "error": "Could not connect to the database.",
            "details": str(error),
        }), 500

    finally:
        if connection is not None:
            connection.close()


# ---------------------------------------------------------
# USERS
# ---------------------------------------------------------

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "A JSON body is required."
        }), 400

    required_fields = [
        "full_name",
        "email",
        "username",
        "password",
        "birth_date",
        "account_status",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in data or data[field] in (None, "")
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "missing_fields": missing_fields,
        }), 400

    if data["account_status"] not in VALID_USER_STATUSES:
        return jsonify({
            "error": "Invalid account status.",
            "valid_statuses": VALID_USER_STATUSES,
        }), 400

    is_delinquent = data.get("is_delinquent", False)

    if not isinstance(is_delinquent, bool):
        return jsonify({
            "error": "is_delinquent must be true or false."
        }), 400

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO lyfter_car_rental.users (
                    full_name,
                    email,
                    username,
                    password,
                    birth_date,
                    account_status,
                    is_delinquent
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING
                    id,
                    full_name,
                    email,
                    username,
                    birth_date,
                    account_status,
                    is_delinquent;
                """,
                (
                    data["full_name"],
                    data["email"],
                    data["username"],
                    data["password"],
                    data["birth_date"],
                    data["account_status"],
                    is_delinquent,
                ),
            )

            new_user = cursor.fetchone()

        connection.commit()

        return jsonify(new_user), 201

    except IntegrityError:
        if connection is not None:
            connection.rollback()

        return jsonify({
            "error": "The email or username already exists."
        }), 409

    except DatabaseError as error:
        if connection is not None:
            connection.rollback()

        return jsonify({
            "error": "Could not create the user.",
            "details": str(error),
        }), 500

    finally:
        if connection is not None:
            connection.close()


@app.route("/users", methods=["GET"])
def get_users():
    conditions = []
    values = []

    for column, value in request.args.items():
        if column not in USER_FILTER_COLUMNS:
            return jsonify({
                "error": f"Invalid filter: {column}",
                "allowed_filters": sorted(USER_FILTER_COLUMNS),
            }), 400

        conditions.append(f"{column} = %s")
        values.append(value)

    query = """
        SELECT
            id,
            full_name,
            email,
            username,
            birth_date,
            account_status,
            is_delinquent
        FROM lyfter_car_rental.users
    """

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id;"

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(query, values)
            users = cursor.fetchall()

        return jsonify(users), 200

    except DatabaseError as error:
        return jsonify({
            "error": "Could not retrieve users.",
            "details": str(error),
        }), 500

    finally:
        if connection is not None:
            connection.close()


@app.route("/users/<int:user_id>/status", methods=["PATCH"])
def update_user_status(user_id):
    data = request.get_json(silent=True)

    if not data or "account_status" not in data:
        return jsonify({
            "error": "account_status is required."
        }), 400

    new_status = data["account_status"]

    if new_status not in VALID_USER_STATUSES:
        return jsonify({
            "error": "Invalid account status.",
            "valid_statuses": VALID_USER_STATUSES,
        }), 400

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE lyfter_car_rental.users
                SET account_status = %s
                WHERE id = %s
                RETURNING
                    id,
                    full_name,
                    email,
                    username,
                    birth_date,
                    account_status,
                    is_delinquent;
                """,
                (new_status, user_id),
            )

            updated_user = cursor.fetchone()

        if updated_user is None:
            connection.rollback()

            return jsonify({
                "error": "User not found."
            }), 404

        connection.commit()

        return jsonify(updated_user), 200

    except DatabaseError as error:
        if connection is not None:
            connection.rollback()

        return jsonify({
            "error": "Could not update the user status.",
            "details": str(error),
        }), 500

    finally:
        if connection is not None:
            connection.close()


@app.route("/users/<int:user_id>/delinquent", methods=["PATCH"])
def update_user_delinquent_status(user_id):
    data = request.get_json(silent=True)

    if not data or "is_delinquent" not in data:
        return jsonify({
            "error": "is_delinquent is required."
        }), 400

    is_delinquent = data["is_delinquent"]

    if not isinstance(is_delinquent, bool):
        return jsonify({
            "error": "is_delinquent must be true or false."
        }), 400

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE lyfter_car_rental.users
                SET is_delinquent = %s
                WHERE id = %s
                RETURNING
                    id,
                    full_name,
                    email,
                    username,
                    birth_date,
                    account_status,
                    is_delinquent;
                """,
                (is_delinquent, user_id),
            )

            updated_user = cursor.fetchone()

        if updated_user is None:
            connection.rollback()

            return jsonify({
                "error": "User not found."
            }), 404

        connection.commit()

        return jsonify(updated_user), 200

    except DatabaseError as error:
        if connection is not None:
            connection.rollback()

        return jsonify({
            "error": "Could not update the delinquent status.",
            "details": str(error),
        }), 500

    finally:
        if connection is not None:
            connection.close()


# ---------------------------------------------------------
# CARS
# ---------------------------------------------------------

@app.route("/cars", methods=["POST"])
def create_car():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "A JSON body is required."
        }), 400

    required_fields = [
        "brand",
        "model",
        "manufacturing_year",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in data or data[field] in (None, "")
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "missing_fields": missing_fields,
        }), 400

    if not isinstance(data["manufacturing_year"], int):
        return jsonify({
            "error": "manufacturing_year must be an integer."
        }), 400

    if (
        "car_status" in data
        and data["car_status"] != "available"
    ):
        return jsonify({
            "error": (
                "A new car must have available as its initial status."
            )
        }), 400

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO lyfter_car_rental.cars (
                    brand,
                    model,
                    manufacturing_year,
                    car_status
                )
                VALUES (%s, %s, %s, 'available')
                RETURNING
                    id,
                    brand,
                    model,
                    manufacturing_year,
                    car_status;
                """,
                (
                    data["brand"],
                    data["model"],
                    data["manufacturing_year"],
                ),
            )

            new_car = cursor.fetchone()

        connection.commit()

        return jsonify(new_car), 201

    except DatabaseError as error:
        if connection is not None:
            connection.rollback()

        return jsonify({
            "error": "Could not create the car.",
            "details": str(error),
        }), 500

    finally:
        if connection is not None:
            connection.close()


@app.route("/cars", methods=["GET"])
def get_cars():
    conditions = []
    values = []

    for column, value in request.args.items():
        if column not in CAR_FILTER_COLUMNS:
            return jsonify({
                "error": f"Invalid filter: {column}",
                "allowed_filters": sorted(CAR_FILTER_COLUMNS),
            }), 400

        conditions.append(f"{column} = %s")
        values.append(value)

    query = """
        SELECT
            id,
            brand,
            model,
            manufacturing_year,
            car_status
        FROM lyfter_car_rental.cars
    """

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id;"

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(query, values)
            cars = cursor.fetchall()

        return jsonify(cars), 200

    except DatabaseError as error:
        return jsonify({
            "error": "Could not retrieve cars.",
            "details": str(error),
        }), 500

    finally:
        if connection is not None:
            connection.close()


@app.route("/cars/<int:car_id>/status", methods=["PATCH"])
def update_car_status(car_id):
    data = request.get_json(silent=True)

    if not data or "car_status" not in data:
        return jsonify({
            "error": "car_status is required."
        }), 400

    new_status = data["car_status"]

    if new_status not in VALID_CAR_STATUSES:
        return jsonify({
            "error": "Invalid car status.",
            "valid_statuses": VALID_CAR_STATUSES,
        }), 400

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE lyfter_car_rental.cars
                SET car_status = %s
                WHERE id = %s
                RETURNING
                    id,
                    brand,
                    model,
                    manufacturing_year,
                    car_status;
                """,
                (new_status, car_id),
            )

            updated_car = cursor.fetchone()

        if updated_car is None:
            connection.rollback()

            return jsonify({
                "error": "Car not found."
            }), 404

        connection.commit()

        return jsonify(updated_car), 200

    except DatabaseError as error:
        if connection is not None:
            connection.rollback()

        return jsonify({
            "error": "Could not update the car status.",
            "details": str(error),
        }), 500

    finally:
        if connection is not None:
            connection.close()


# ---------------------------------------------------------
# RENTALS
# ---------------------------------------------------------

@app.route("/rentals", methods=["POST"])
def create_rental():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "A JSON body is required."
        }), 400

    required_fields = [
        "user_id",
        "car_id",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in data or data[field] in (None, "")
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "missing_fields": missing_fields,
        }), 400

    if not isinstance(data["user_id"], int):
        return jsonify({
            "error": "user_id must be an integer."
        }), 400

    if not isinstance(data["car_id"], int):
        return jsonify({
            "error": "car_id must be an integer."
        }), 400

    rental_status = data.get("rental_status", "active")

    if rental_status not in INITIAL_RENTAL_STATUSES:
        return jsonify({
            "error": "Invalid initial rental status.",
            "valid_initial_statuses": INITIAL_RENTAL_STATUSES,
        }), 400

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    account_status,
                    is_delinquent
                FROM lyfter_car_rental.users
                WHERE id = %s
                FOR UPDATE;
                """,
                (data["user_id"],),
            )

            user = cursor.fetchone()

            if user is None:
                connection.rollback()

                return jsonify({
                    "error": "User not found."
                }), 404

            if user["account_status"] != "active":
                connection.rollback()

                return jsonify({
                    "error": "The user account is not active."
                }), 409

            if user["is_delinquent"]:
                connection.rollback()

                return jsonify({
                    "error": "The user is marked as delinquent."
                }), 409

            cursor.execute(
                """
                SELECT
                    id,
                    car_status
                FROM lyfter_car_rental.cars
                WHERE id = %s
                FOR UPDATE;
                """,
                (data["car_id"],),
            )

            car = cursor.fetchone()

            if car is None:
                connection.rollback()

                return jsonify({
                    "error": "Car not found."
                }), 404

            if car["car_status"] != "available":
                connection.rollback()

                return jsonify({
                    "error": "The car is not available."
                }), 409

            cursor.execute(
                """
                INSERT INTO lyfter_car_rental.rentals (
                    user_id,
                    car_id,
                    rental_status
                )
                VALUES (%s, %s, %s)
                RETURNING
                    id,
                    user_id,
                    car_id,
                    rental_date,
                    rental_status;
                """,
                (
                    data["user_id"],
                    data["car_id"],
                    rental_status,
                ),
            )

            new_rental = cursor.fetchone()

            cursor.execute(
                """
                UPDATE lyfter_car_rental.cars
                SET car_status = 'rented'
                WHERE id = %s;
                """,
                (data["car_id"],),
            )

        connection.commit()

        return jsonify(new_rental), 201

    except DatabaseError as error:
        if connection is not None:
            connection.rollback()

        return jsonify({
            "error": "Could not create the rental.",
            "details": str(error),
        }), 500

    finally:
        if connection is not None:
            connection.close()


@app.route("/rentals", methods=["GET"])
def get_rentals():
    conditions = []
    values = []

    for column, value in request.args.items():
        if column not in RENTAL_FILTER_COLUMNS:
            return jsonify({
                "error": f"Invalid filter: {column}",
                "allowed_filters": sorted(RENTAL_FILTER_COLUMNS),
            }), 400

        conditions.append(f"r.{column} = %s")
        values.append(value)

    query = """
        SELECT
            r.id,
            r.user_id,
            u.full_name AS user_name,
            r.car_id,
            c.brand AS car_brand,
            c.model AS car_model,
            r.rental_date,
            r.rental_status
        FROM lyfter_car_rental.rentals AS r
        INNER JOIN lyfter_car_rental.users AS u
            ON r.user_id = u.id
        INNER JOIN lyfter_car_rental.cars AS c
            ON r.car_id = c.id
    """

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY r.id;"

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(query, values)
            rentals = cursor.fetchall()

        return jsonify(rentals), 200

    except DatabaseError as error:
        return jsonify({
            "error": "Could not retrieve rentals.",
            "details": str(error),
        }), 500

    finally:
        if connection is not None:
            connection.close()


@app.route("/rentals/<int:rental_id>/status", methods=["PATCH"])
def update_rental_status(rental_id):
    data = request.get_json(silent=True)

    if not data or "rental_status" not in data:
        return jsonify({
            "error": "rental_status is required."
        }), 400

    new_status = data["rental_status"]

    if new_status not in VALID_RENTAL_STATUSES:
        return jsonify({
            "error": "Invalid rental status.",
            "valid_statuses": VALID_RENTAL_STATUSES,
        }), 400

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    car_id,
                    rental_status
                FROM lyfter_car_rental.rentals
                WHERE id = %s
                FOR UPDATE;
                """,
                (rental_id,),
            )

            rental = cursor.fetchone()

            if rental is None:
                connection.rollback()

                return jsonify({
                    "error": "Rental not found."
                }), 404

            current_status = rental["rental_status"]

            allowed_transitions = RENTAL_STATUS_TRANSITIONS.get(
                current_status,
                [],
            )

            if new_status not in allowed_transitions:
                connection.rollback()

                return jsonify({
                    "error": (
                        f"Cannot change rental status from "
                        f"{current_status} to {new_status}."
                    ),
                    "allowed_transitions": allowed_transitions,
                }), 409

            cursor.execute(
                """
                UPDATE lyfter_car_rental.rentals
                SET rental_status = %s
                WHERE id = %s
                RETURNING
                    id,
                    user_id,
                    car_id,
                    rental_date,
                    rental_status;
                """,
                (new_status, rental_id),
            )

            updated_rental = cursor.fetchone()

            if new_status in ["completed", "cancelled"]:
                cursor.execute(
                    """
                    UPDATE lyfter_car_rental.cars
                    SET car_status = 'available'
                    WHERE id = %s;
                    """,
                    (rental["car_id"],),
                )

            if new_status == "active":
                cursor.execute(
                    """
                    UPDATE lyfter_car_rental.cars
                    SET car_status = 'rented'
                    WHERE id = %s;
                    """,
                    (rental["car_id"],),
                )

        connection.commit()

        return jsonify(updated_rental), 200

    except DatabaseError as error:
        if connection is not None:
            connection.rollback()

        return jsonify({
            "error": "Could not update the rental status.",
            "details": str(error),
        }), 500

    finally:
        if connection is not None:
            connection.close()


@app.route("/rentals/<int:rental_id>/complete", methods=["PATCH"])
def complete_rental(rental_id):
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    car_id,
                    rental_status
                FROM lyfter_car_rental.rentals
                WHERE id = %s
                FOR UPDATE;
                """,
                (rental_id,),
            )

            rental = cursor.fetchone()

            if rental is None:
                connection.rollback()

                return jsonify({
                    "error": "Rental not found."
                }), 404

            if rental["rental_status"] != "active":
                connection.rollback()

                return jsonify({
                    "error": "The rental is not active."
                }), 409

            cursor.execute(
                """
                UPDATE lyfter_car_rental.rentals
                SET rental_status = 'completed'
                WHERE id = %s
                RETURNING
                    id,
                    user_id,
                    car_id,
                    rental_date,
                    rental_status;
                """,
                (rental_id,),
            )

            completed_rental = cursor.fetchone()

            cursor.execute(
                """
                UPDATE lyfter_car_rental.cars
                SET car_status = 'available'
                WHERE id = %s;
                """,
                (rental["car_id"],),
            )

        connection.commit()

        return jsonify(completed_rental), 200

    except DatabaseError as error:
        if connection is not None:
            connection.rollback()

        return jsonify({
            "error": "Could not complete the rental.",
            "details": str(error),
        }), 500

    finally:
        if connection is not None:
            connection.close()


# ---------------------------------------------------------
# START APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)