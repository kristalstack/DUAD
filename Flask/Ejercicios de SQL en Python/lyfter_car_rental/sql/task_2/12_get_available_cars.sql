SELECT
    id,
    brand,
    model,
    manufacturing_year,
    car_status
FROM lyfter_car_rental.cars
WHERE car_status = 'available'
ORDER BY brand, model;