BEGIN;

DO $$
DECLARE
    v_user_id INT := 1;
    v_bill_id INT;
    v_total NUMERIC(10,2) := 0;

    v_product_id INT;
    v_quantity INT;
    v_price NUMERIC(10,2);
    v_stock INT;

    products_to_buy INT[] := ARRAY[1, 2, 3];
    quantities_to_buy INT[] := ARRAY[1, 2, 1];

    i INT;
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM users_app WHERE id = v_user_id
    ) THEN
        RAISE EXCEPTION 'El usuario con ID % no existe', v_user_id;
    END IF;

    FOR i IN 1..array_length(products_to_buy, 1) LOOP
        v_product_id := products_to_buy[i];
        v_quantity := quantities_to_buy[i];

        SELECT price, stock
        INTO v_price, v_stock
        FROM products
        WHERE id = v_product_id;

        IF NOT FOUND THEN
            RAISE EXCEPTION 'El producto con ID % no existe', v_product_id;
        END IF;

        IF v_stock < v_quantity THEN
            RAISE EXCEPTION 'Stock insuficiente para el producto ID %', v_product_id;
        END IF;
    END LOOP;

    INSERT INTO bills (user_id, status)
    VALUES (v_user_id, 'Activa')
    RETURNING id INTO v_bill_id;

    FOR i IN 1..array_length(products_to_buy, 1) LOOP
        v_product_id := products_to_buy[i];
        v_quantity := quantities_to_buy[i];

        SELECT price
        INTO v_price
        FROM products
        WHERE id = v_product_id;

        INSERT INTO bill_items (
            bill_id,
            product_id,
            quantity,
            unit_price,
            subtotal
        )
        VALUES (
            v_bill_id,
            v_product_id,
            v_quantity,
            v_price,
            v_price * v_quantity
        );

        UPDATE products
        SET stock = stock - v_quantity
        WHERE id = v_product_id;

        v_total := v_total + (v_price * v_quantity);
    END LOOP;

    UPDATE bills
    SET total = v_total
    WHERE id = v_bill_id;

    RAISE NOTICE 'Compra realizada correctamente. Factura ID: %, Total: %', v_bill_id, v_total;
END $$;

COMMIT;