"""Supercharged requests to handle errors from the API."""
import logging
from functools import wraps

import requests

logger = logging.getLogger(__name__)


def add_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func  # returning func means func can still be used normally
    return decorator


@add_method(requests)
def supercharged_requests(*args, **kwargs):
    retrieved_data = requests.get(*args, **kwargs)
    counter_requests = 0
    while retrieved_data.status_code != 200:
        logger.warning("Error from API. Requesting again...")
        retrieved_data = requests.get(*args, **kwargs)
        counter_requests += 1
        if counter_requests > 30:
            logger.warning("DEAD API")
    return retrieved_data
