"""Get nearest city."""
import logging
import requests
from .. import config
from .queries import query_city

logger = logging.getLogger(__name__)

def get_nearest_city(
    latitude: float,
    longitude: float,
) -> str:
    """blabla"""
    n_iter = 0
    radplus = config.data.get("Nearest_city").get(
        "Binary_search").get("initial_upper_bound_radius", 10000)
    radmoins = config.data.get("Nearest_city").get(
        "Binary_search").get("lower_bound_radius", 0)
    max_iter_before_increased_radius = config.data.get("Nearest_city").get(
        "Binary_search").get("iter_before_increased_radius", 10)
    overpass_url = config.data.get("API").get(
        "overpass_url", "http://overpass-api.de/api/interpreter")

    rad = (radplus + radmoins) / 2
    overpass_query = query_city(
        rad=rad, latitude=latitude, longitude=longitude)
    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    data = response.json()

    while len(data['elements']) != 1:
        if n_iter == max_iter_before_increased_radius:
            n_iter = 0
            radplus += 1000
            rad = (radplus + radmoins) / 2
            overpass_query = query_city(
                rad=rad, latitude=latitude, longitude=longitude)
            response = requests.get(overpass_url,
                                    params={'data': overpass_query})
            data = response.json()
        elif len(data['elements']) == 0:
            n_iter += 1
            radmoins = rad
            rad = (radplus + radmoins) / 2
            overpass_query = query_city(
                rad=rad, latitude=latitude, longitude=longitude)
            response = requests.get(overpass_url,
                                    params={'data': overpass_query})
            data = response.json()
        elif len(data['elements']) >= 2:
            n_iter = 0
            radplus = rad
            rad = (radplus + radmoins) / 2
            overpass_query = query_city(
                rad=rad, latitude=latitude, longitude=longitude)
            response = requests.get(overpass_url,
                                    params={'data': overpass_query})
            data = response.json()
    return data['elements'][0]['tags']['name']
