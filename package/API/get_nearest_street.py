"""Get nearest street."""
import logging
import requests
from typing import Dict
from .. import config
from .queries import query_street

logger = logging.getLogger(__name__)


def get_nearest_street(
    latitude: float,
    longitude: float
) -> Dict:
    """."""
    # Get hyperparameters from yaml.
    radplus = config.data.get("Nearest_street").get(
        "Binary_search").get("initial_upper_bound_radius", 100)
    radmoins = config.data.get("Nearest_street").get(
        "Binary_search").get("lower_bound_radius", 0)
    max_iter_before_increased_radius = config.data.get("Nearest_street").get(
        "Binary_search").get("iter_before_increased_radius", 10)
    overpass_url = config.data.get("API").get(
        "overpass_url", "http://overpass-api.de/api/interpreter")

    rad = (radplus + radmoins) / 2
    overpass_query = query_street(
        rad=rad, latitude=latitude, longitude=longitude)
    logging.info(
        "Using openstreetmap API to get nearest street. This can take a while.. ☕")

    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    data = response.json()
    logging.info("Got the response")
    ways = [x for x in data['elements'] if x['type'] == 'way']

    n_iter = 0
    while len(ways) != 1:
        # Increase radius after 10 unsucessful iterartions.
        if n_iter == max_iter_before_increased_radius:
            n_iter = 0
            radplus += 1000

        else:
            # Binary search algorithm.
            if ways:
                n_iter = 0
                radplus = rad
            else:
                n_iter += 1
                radmoins = rad

        rad = (radplus + radmoins) / 2
        overpass_query = query_street(
            rad=rad, latitude=latitude, longitude=longitude)
        response = requests.get(overpass_url,
                                params={'data': overpass_query})
        data = response.json()
        ways = [x for x in data['elements'] if x['type'] == 'way']

    return ways[0]
