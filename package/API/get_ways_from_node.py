"""Get ways from node."""
from typing import List, Tuple

from .queries import query_nodes, query_ways
from .supercharged_requests import requests


def get_ways_from_node(
        list_node: List[int]
) -> List[Tuple]:
    """Find the ways that have common node with your street.

    :param list_node: list of the nodes in your street.

    return list_ways: list of ways that have common nodes with your street
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    list_ways = []
    for id_node in list_node:
        overpass_query_get_node = query_nodes(id_node)
        response = requests.supercharged_requests(overpass_url,
                                                  params={'data': overpass_query_get_node})
        node = response.json()
        latitude = node['elements'][0]['lat']
        longitude = node['elements'][0]['lon']
        overpass_query_get_ways = query_ways(
            latitude=latitude, longitude=longitude)
        response = requests.supercharged_requests(overpass_url,
                                                  params={'data': overpass_query_get_ways})
        ways = [x for x in response.json()['elements'] if x['type'] == 'way']
        names = [way['tags']['name'] for way in ways]
        list_ways.append(((list(set(names))), (latitude, longitude)))
    return list_ways
