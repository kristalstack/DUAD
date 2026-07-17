SELECT
    c.id AS car_id,
    c.brand,
    c.model,
    c.manufacturing_year,
    c.car_status,
    u.id AS user_id,
    u.full_name,
    u.email,
    r.id AS rental_id,
    r.rental_date,
    r.rental_status
FROM lyfter_car_rental.cars AS c
INNER JOIN lyfter_car_rental.rentals AS r
    ON c.id = r.car_id
INNER JOIN lyfter_car_rental.users AS u
    ON r.user_id = u.id
WHERE c.car_status = 'rented'
  AND r.rental_status = 'active'
ORDER BY r.rental_date;