import json
import logging
from typing import Any, Callable

from redis.exceptions import RedisError

from redis_client import redis_client


logger = logging.getLogger(__name__)

PRODUCTS_KEY = "products:all"

# Cinco minutos.
CACHE_TTL_SECONDS = 300


def execute_cache_operation(
    operation: Callable[[], Any],
    default: Any = None,
):
    try:
        return operation()
    except RedisError:
        logger.exception("Redis operation failed.")
        return default


def get_cached_json(key: str):
    def operation():
        data = redis_client.get(key)

        if data is None:
            return None

        return json.loads(data)

    return execute_cache_operation(
        operation,
        default=None,
    )


def set_cached_json(
    key: str,
    value: Any,
    ttl: int = CACHE_TTL_SECONDS,
) -> bool:
    def operation():
        redis_client.set(
            key,
            json.dumps(value),
            ex=ttl,
        )
        return True

    return execute_cache_operation(
        operation,
        default=False,
    )


def delete_cache_keys(*keys: str) -> bool:
    def operation():
        redis_client.delete(*keys)
        return True

    return execute_cache_operation(
        operation,
        default=False,
    )


def get_products_cache():
    return get_cached_json(PRODUCTS_KEY)


def set_products_cache(products) -> bool:
    return set_cached_json(
        PRODUCTS_KEY,
        products,
    )


def get_product_cache(product_id: int):
    return get_cached_json(
        f"product:{product_id}"
    )


def set_product_cache(product: dict) -> bool:
    return set_cached_json(
        f"product:{product['id']}",
        product,
    )


def invalidate_product_cache(product_id: int) -> bool:
    return delete_cache_keys(
        f"product:{product_id}"
    )


def invalidate_products_cache() -> bool:
    return delete_cache_keys(
        PRODUCTS_KEY
    )


def invalidate_product_and_list_cache(
    product_id: int,
) -> bool:
    return delete_cache_keys(
        f"product:{product_id}",
        PRODUCTS_KEY,
    )