DO $$
DECLARE
    selected_user_id INTEGER := 2;
    selected_car_id INTEGER := 3;
    current_user_status VARCHAR(20);
    current_car_status VARCHAR(20);
BEGIN
    SELECT account_status
    INTO current_user_status
    FROM lyfter_car_rental.users
    WHERE id = selected_user_id;

    IF current_user_status IS NULL THEN
        RAISE EXCEPTION 'The user does not exist.';
    END IF;

    IF current_user_status <> 'active' THEN
        RAISE EXCEPTION 'The user account is not active.';
    END IF;

    SELECT car_status
    INTO current_car_status
    FROM lyfter_car_rental.cars
    WHERE id = selected_car_id;

    IF current_car_status IS NULL THEN
        RAISE EXCEPTION 'The car does not exist.';
    END IF;

    IF current_car_status <> 'available' THEN
        RAISE EXCEPTION 'The car is not available.';
    END IF;

    INSERT INTO lyfter_car_rental.rentals (
        user_id,
        car_id,
        rental_status
    )
    VALUES (
        selected_user_id,
        selected_car_id,
        'active'
    );

    UPDATE lyfter_car_rental.cars
    SET car_status = 'rented'
    WHERE id = selected_car_id;
END $$;