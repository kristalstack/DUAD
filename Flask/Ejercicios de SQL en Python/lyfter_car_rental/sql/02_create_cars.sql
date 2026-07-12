DROP TABLE IF EXISTS lyfter_car_rental.cars CASCADE;

CREATE TABLE lyfter_car_rental.cars (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(80) NOT NULL,
    manufacturing_year INTEGER NOT NULL
        CHECK (
            manufacturing_year >= 1900
            AND manufacturing_year <= EXTRACT(YEAR FROM CURRENT_DATE)::INTEGER + 1
        ),
    car_status VARCHAR(20) NOT NULL
        CHECK (
            car_status IN (
                'available',
                'rented',
                'maintenance',
                'unavailable'
            )
        )
);

INSERT INTO lyfter_car_rental.cars (
    brand,
    model,
    manufacturing_year,
    car_status
)
VALUES
    ('Toyota', 'Corolla', 2022, 'available'),
    ('Toyota', 'RAV4', 2023, 'rented'),
    ('Toyota', 'Yaris', 2021, 'available'),
    ('Honda', 'Civic', 2022, 'available'),
    ('Honda', 'CR-V', 2024, 'rented'),
    ('Honda', 'Accord', 2020, 'maintenance'),
    ('Nissan', 'Sentra', 2021, 'available'),
    ('Nissan', 'Versa', 2023, 'available'),
    ('Nissan', 'X-Trail', 2022, 'rented'),
    ('Hyundai', 'Elantra', 2021, 'available'),
    ('Hyundai', 'Tucson', 2023, 'maintenance'),
    ('Hyundai', 'Accent', 2020, 'available'),
    ('Kia', 'Rio', 2022, 'available'),
    ('Kia', 'Sportage', 2024, 'rented'),
    ('Kia', 'Seltos', 2023, 'available'),
    ('Ford', 'Escape', 2021, 'available'),
    ('Ford', 'Explorer', 2022, 'maintenance'),
    ('Ford', 'Mustang', 2020, 'unavailable'),
    ('Chevrolet', 'Spark', 2021, 'available'),
    ('Chevrolet', 'Tracker', 2023, 'rented'),
    ('Chevrolet', 'Tahoe', 2022, 'available'),
    ('Mazda', 'Mazda 3', 2022, 'available'),
    ('Mazda', 'CX-5', 2024, 'rented'),
    ('Mazda', 'CX-30', 2023, 'available'),
    ('Volkswagen', 'Jetta', 2021, 'maintenance'),
    ('Volkswagen', 'Tiguan', 2022, 'available'),
    ('Volkswagen', 'Taos', 2023, 'rented'),
    ('Renault', 'Duster', 2021, 'available'),
    ('Renault', 'Kwid', 2022, 'available'),
    ('Renault', 'Captur', 2020, 'unavailable'),
    ('Suzuki', 'Swift', 2023, 'available'),
    ('Suzuki', 'Vitara', 2022, 'rented'),
    ('Suzuki', 'Jimny', 2024, 'available'),
    ('Mitsubishi', 'Outlander', 2021, 'maintenance'),
    ('Mitsubishi', 'ASX', 2022, 'available'),
    ('Subaru', 'Forester', 2023, 'rented'),
    ('Subaru', 'Impreza', 2021, 'available'),
    ('BMW', 'X1', 2022, 'available'),
    ('BMW', '320i', 2021, 'maintenance'),
    ('Mercedes-Benz', 'A-Class', 2023, 'rented'),
    ('Mercedes-Benz', 'GLA', 2022, 'available'),
    ('Audi', 'A3', 2021, 'available'),
    ('Audi', 'Q3', 2023, 'rented'),
    ('Jeep', 'Renegade', 2022, 'available'),
    ('Jeep', 'Compass', 2021, 'maintenance'),
    ('Peugeot', '208', 2023, 'available'),
    ('Peugeot', '2008', 2022, 'rented'),
    ('Fiat', '500', 2021, 'available'),
    ('Fiat', 'Pulse', 2023, 'available'),
    ('Volvo', 'XC40', 2024, 'rented');