DROP TABLE IF EXISTS lyfter_car_rental.rentals;

CREATE TABLE lyfter_car_rental.rentals (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id INTEGER NOT NULL,
    car_id INTEGER NOT NULL,

    rental_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    rental_status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (
            rental_status IN (
                'reserved',
                'active',
                'completed',
                'cancelled'
            )
        ),

    CONSTRAINT fk_rentals_user
        FOREIGN KEY (user_id)
        REFERENCES lyfter_car_rental.users(id),

    CONSTRAINT fk_rentals_car
        FOREIGN KEY (car_id)
        REFERENCES lyfter_car_rental.cars(id)
);