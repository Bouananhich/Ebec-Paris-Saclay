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
    #Get hyperparameters from yaml.
    radplus = config.data.get("Nearest_street").get(
        "Binary_search").get("initial_upper_bound_radius", 10000)
    radmoins = config.data.get("Nearest_street").get(
        "Binary_search").get("lower_bound_radius", 0)
    max_iter_before_increased_radius = config.data.get("Nearest_street").get(
        "Binary_search").get("iter_before_increased_radius", 10)
    overpass_url = config.data.get("API").get(
        "overpass_url", "http://overpass-api.de/api/interpreter")
    rad = (radplus + radmoins) / 2
    overpass_query = query_street(
        rad=rad, latitude=latitude, longitude=longitude)
    logging.info("Using openstreetmap API. This can take a while.. ☕")
    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    data = response.json()
    logging.info("Got the response")
    ways = [x for x in data['elements'] if x['type'] == 'way']

    n_iter = 0
    while len(ways) != 1:
        #Increase radius after 10 unsucessful iterartions.
        if not n_iter % max_iter_before_increased_radius:
            radplus += 1000
            rad = (radplus + radmoins) / 2

        else:
            #Binary search algorithm.
            if len(ways) == 0:
                n_iter += 1
                radmoins = rad
            else:
                n_iter = 0
                radplus = rad
            rad = (radplus + radmoins) / 2

        overpass_query = query_street(
            rad=rad, latitude=latitude, longitude=longitude)
        response = requests.get(overpass_url,
                                params={'data': overpass_query})
        data = response.json()
        ways = [x for x in data['elements'] if x['type'] == 'way']

    return ways[0]
