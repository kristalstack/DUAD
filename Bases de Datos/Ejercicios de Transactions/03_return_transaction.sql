BEGIN;

DO $$
DECLARE
    v_bill_id INT := 1;
    item RECORD;
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM bills
        WHERE id = v_bill_id
    ) THEN
        RAISE EXCEPTION 'La factura % no existe', v_bill_id;
    END IF;

    IF EXISTS (
        SELECT 1
        FROM bills
        WHERE id = v_bill_id
        AND status = 'Retornada'
    ) THEN
        RAISE EXCEPTION 'La factura % ya fue retornada', v_bill_id;
    END IF;

    FOR item IN
        SELECT product_id, quantity
        FROM bill_items
        WHERE bill_id = v_bill_id
    LOOP
        UPDATE products
        SET stock = stock + item.quantity
        WHERE id = item.product_id;
    END LOOP;

    UPDATE bills
    SET status = 'Retornada'
    WHERE id = v_bill_id;

    RAISE NOTICE 'Retorno procesado correctamente para la factura %.', v_bill_id;
END $$;

COMMIT;