from .extensions import cache


def product_key(product_id):
    return f"product:{product_id}"


def products_list_key():
    return f"products:list:v{cache.get('products_version') or 1}"


def invalidate_products(product_id=None):
    cache.set("products_version", int(cache.get("products_version") or 1) + 1, timeout=0)
    if product_id is not None:
        cache.delete(product_key(product_id))


def invoice_key(number):
    return f"invoice:{number}"


def invalidate_invoice(number):
    cache.delete(invoice_key(number))

