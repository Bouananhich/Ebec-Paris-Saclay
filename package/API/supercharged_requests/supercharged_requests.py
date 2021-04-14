"""Supercharged requests to handle errors from the API."""
import asyncio
import logging
from functools import wraps
from typing import Any, List, Tuple

import httpx
import requests

from ... import config
from .. import queries

logger = logging.getLogger(__name__)
overpass_url = config.data.get("API").get(
    "overpass_url", "http://overpass-api.de/api/interpreter")


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
    retrieved_data = requests.get(url=overpass_url, *args, **kwargs)
    counter_requests = 0
    while retrieved_data.status_code != 200:
        logger.warning("Error from API. Requesting again...")
        retrieved_data = requests.get(url=overpass_url, *args, **kwargs)
        counter_requests += 1
        if counter_requests > 30:
            logger.warning("DEAD API")

    return retrieved_data


@add_method(requests)
async def async_request(
    sem: Any,
    id_node: int,
    delay_async: int,
    *args,
    **kwargs,
) -> Tuple[List, Tuple]:
    async with sem, httpx.AsyncClient() as client:
        timeout = httpx.Timeout(800.0)
        await asyncio.sleep(delay_async * 0.01)
        overpass_query_get_node = queries.query_nodes(id_node)
        retrieved_data = await client.get(
            f"{overpass_url}?data={overpass_query_get_node}", timeout=timeout)
        counter_requests = 0
        while retrieved_data.status_code != 200:
            logger.warning("Error from API. Requesting again...")
            retrieved_data = await client.get(
                f"{overpass_url}?data={overpass_query_get_node}", timeout=timeout)
            counter_requests += 1

        node = retrieved_data.json()
        latitude = node['elements'][0]['lat']
        longitude = node['elements'][0]['lon']

        overpass_query_get_ways = queries.query_ways(
            latitude=latitude, longitude=longitude)

        retrieved_data = await client.get(
            f"{overpass_url}?data={overpass_query_get_ways}", timeout=timeout)
        counter_requests = 0
        while retrieved_data.status_code != 200:
            logger.warning("Error from API. Requesting again...")
            retrieved_data = await client.get(
                f"{overpass_url}?data={overpass_query_get_node}", timeout=timeout)
            counter_requests += 1

        ways = [x for x in retrieved_data.json()['elements']
                if x['type'] == 'way']
        names = [way['tags']['name'] for way in ways]
        return ((list(set(names))), (latitude, longitude))
