"""Get ways from node."""
import requests
from typing import List, Tuple


def get_ways_from_node(
    list_node: List[int]
) -> List[Tuple]:
    """."""
    overpass_url = "http://overpass-api.de/api/interpreter"
    list_ways = []
    for id_node in list_node:

        overpass_query_get_node = f"""[out:json][timeout:25];
                            node({id_node});
                            out;
                            """
        response = requests.get(overpass_url,
                                params={'data': overpass_query_get_node})
        node = response.json()
        latitude = node['elements'][0]['lat']
        longitude = node['elements'][0]['lon']
        overpass_query_get_ways = ways_query(
            latitude=latitude, longitude=longitude)
        response = requests.get(overpass_url,
                                params={'data': overpass_query_get_ways})
        ways = [x for x in response.json()['elements'] if x['type'] == 'way']
        names = [way['tags']['name'] for way in ways]
        list_ways.append(((list(set(names))), (latitude, longitude)))
    return list_ways


def ways_query(
    latitude: float,
    longitude: float,
) -> str:
    overpass_query_get_ways = f"""[out:json];
                                    way
                                      (around:2,{latitude},{longitude})
                                      [name];
                                    (._;>;);
                                    out;"""
    return overpass_query_get_ways
