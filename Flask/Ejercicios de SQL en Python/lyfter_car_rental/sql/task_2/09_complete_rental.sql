DO $$
DECLARE
    selected_rental_id INTEGER := 1;
    selected_car_id INTEGER;
    current_rental_status VARCHAR(20);
BEGIN
    SELECT car_id, rental_status
    INTO selected_car_id, current_rental_status
    FROM lyfter_car_rental.rentals
    WHERE id = selected_rental_id;

    IF selected_car_id IS NULL THEN
        RAISE EXCEPTION 'The rental does not exist.';
    END IF;

    IF current_rental_status <> 'active' THEN
        RAISE EXCEPTION 'The rental is not active.';
    END IF;

    UPDATE lyfter_car_rental.rentals
    SET rental_status = 'completed'
    WHERE id = selected_rental_id;

    UPDATE lyfter_car_rental.cars
    SET car_status = 'available'
    WHERE id = selected_car_id;
END $$;