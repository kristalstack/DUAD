import json

from redis_client import redis_client


PRODUCTS_KEY = "products:all"


def get_products_cache():
    data = redis_client.get(PRODUCTS_KEY)

    if data is None:
        return None

    return json.loads(data)


def set_products_cache(products):
    redis_client.set(
        PRODUCTS_KEY,
        json.dumps(products),
    )


def get_product_cache(product_id):
    key = f"product:{product_id}"

    data = redis_client.get(key)

    if data is None:
        return None

    return json.loads(data)


def set_product_cache(product):
    key = f"product:{product['id']}"

    redis_client.set(
        key,
        json.dumps(product),
    )


def invalidate_product_cache(product_id):
    redis_client.delete(f"product:{product_id}")


def invalidate_products_cache():
    redis_client.delete(PRODUCTS_KEY)