"""Get ways from node."""
import requests
from typing import List, Tuple
from .queries import query_ways, query_nodes


def get_ways_from_node(
    list_node: List[int]
) -> List[Tuple]:
    """."""
    overpass_url = "http://overpass-api.de/api/interpreter"
    list_ways = []
    for id_node in list_node:

        overpass_query_get_node = query_nodes(id_node)
        response = requests.get(overpass_url,
                                params={'data': overpass_query_get_node})
        node = response.json()
        latitude = node['elements'][0]['lat']
        longitude = node['elements'][0]['lon']
        overpass_query_get_ways = query_ways(
            latitude=latitude, longitude=longitude)
        response = requests.get(overpass_url,
                                params={'data': overpass_query_get_ways})
        ways = [x for x in response.json()['elements'] if x['type'] == 'way']
        names = [way['tags']['name'] for way in ways]
        list_ways.append(((list(set(names))), (latitude, longitude)))
    return list_ways
