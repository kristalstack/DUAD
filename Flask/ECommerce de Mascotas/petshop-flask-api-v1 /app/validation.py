from decimal import Decimal, InvalidOperation


def require_json(required=()):
    from flask import request
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, "Se requiere un cuerpo JSON válido"
    missing = [field for field in required if data.get(field) in (None, "")]
    if missing:
        return None, f"Faltan campos requeridos: {', '.join(missing)}"
    return data, None


def positive_int(value, field="quantity"):
    if isinstance(value, bool):
        raise ValueError(f"{field} debe ser un entero positivo")
    result = int(value)
    if result <= 0 or str(result) != str(value):
        raise ValueError(f"{field} debe ser un entero positivo")
    return result


def nonnegative_money(value):
    try:
        result = Decimal(str(value)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        raise ValueError("price debe ser un número válido")
    if result < 0:
        raise ValueError("price no puede ser negativo")
    return result


def country_code(value):
    if not isinstance(value, str):
        raise ValueError("country debe ser un código de país de 2 letras")
    result = value.strip().upper()
    if len(result) != 2 or not result.isalpha():
        raise ValueError("country debe ser un código de país de 2 letras")
    return result
