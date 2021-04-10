"""Useful functions"""
from typing import List, Tuple
from ..API.get_nearest_street import get_nearest_street
from ..API.get_ways_from_node import get_ways_from_node


def get_nodes(
    latitude: float = 48.89535,
    longitude: float = 2.24697,
) -> List[int]:
    """Get nodes near position."""
    street = get_nearest_street(latitude=latitude,
                                longitude=longitude)
    nodes = street.get("nodes", "Error with API")
    return nodes


def get_ways(
    latitude: float = 48.89535,
    longitude: float = 2.24697,
) -> List[Tuple]:
    """Get ways crossing nearest street of point."""
    nodes = get_nodes(latitude=latitude,
                      longitude=longitude)
    ways = get_ways_from_node(list_node=nodes)
    return ways
