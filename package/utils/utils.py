"""Useful functions."""
import logging
from copy import deepcopy
from operator import itemgetter
from typing import Dict, List, Tuple

from numpy import array, cross, dot
from numpy.linalg import norm

from ..API.get_nearest_street import get_nearest_street
from ..API.get_ways_from_node import get_ways_from_node

logger = logging.getLogger(__name__)


def get_nodes(
        latitude: float,
        longitude: float,
) -> List[int]:
    """Get nodes near position.

    :param latitude: latitude of your point.
    :param longitude: longitude of your point.

    return nodes, name: nodes in your street and name of the street
    """
    street = get_nearest_street(latitude=latitude,
                                longitude=longitude)
    name = street.get("tags").get("name")
    nodes = street.get("nodes", "Error with API")
    return nodes, name


def get_ways(
        latitude: float,
        longitude: float,
) -> List[Tuple]:
    """Get ways crossing nearest street of point.

    return list of ways crossing the street containing the
    (latitude, longitude) point
    """
    nodes, name = get_nodes(latitude=latitude,
                            longitude=longitude)
    ways = get_ways_from_node(list_node=nodes)
    return ways, name

def get_road_sections(
        intersection_list: List[Tuple],
        road_name: str,
) -> List[List]:
    """Build road sections in which we can place the coordinates.

    :param interp: Output of get_ways function.
    :param road_name: Used to drop it in intersection_list.

    return sections_list : List[str,str, Tuple(float, float), Tuple(float, float)]
    """
    new_intersection_list = deepcopy(intersection_list)
    sections_list = list()
    new_names_list = list()
    new_coordinates_list = list()
    for i in range(len(new_intersection_list)):
        if len(new_intersection_list[i][0]) > 1:
            if road_name in new_intersection_list[i][0]:
                index_road_name = new_intersection_list[i][0].index(road_name)
                new_intersection_list[i][0].pop(index_road_name)
                new_node_name = '/'.join(new_intersection_list[i][0])
                new_names_list.append(new_node_name)
                new_coordinates_list.append(new_intersection_list[i][1])
    for i in range(1, len(new_names_list)):
        sections_list.append([new_names_list[i - 1], new_names_list[i],
                              new_coordinates_list[i - 1], new_coordinates_list[i]])
    return sections_list


def conversion_list_dict(
    sections_list: List[List],
) -> Dict[Tuple, List]:
    """Convert sections list to a dictionnary.

    :param sections_list: Output of get_road_sections.

    return sections_dict
    """
    sections_dict = {tuple([key1, key2]): list_coordinates for key1,
                     key2, *list_coordinates in sections_list}

    return sections_dict


def distance_from_segment(
        reference: Tuple[float, float],
        coordinates_dict: Dict[Tuple, List],
) -> Dict[Tuple, List]:
    """Compute the distance of a given point to segments.

    :param reference: point.
    :param coordinates_dict: keys are the name of the streets
    that bound the segment, values are list of tuples that
    correspond to the coordinates of the crossings.

    return distance_dict: keys are the name of the streets
    that bound a segment, values are the computed distance
    between the point and the associated segment
    """
    logging.info("Computing shortest segment")
    p3 = array(reference)
    distances_dict = dict()
    for key, (p1, p2) in coordinates_dict.items():
        p1, p2 = array(p1), array(p2)
        distance = norm(cross(p2 - p1, p3 - p1))
        # check if the nearest point is in the segment (p1,p2)
        if dot(p3 - p1, p3 - p2) < 0:
            distances_dict[key] = distance
    if not bool(distances_dict):  # if dict is empty
        for key, (p1, p2) in coordinates_dict.items():
            distance_p1, distance_p2 = norm(
                reference - p1), norm(reference - p2)
            distance = min(distance_p1, distance_p2)
    return distances_dict


def find_optimal(
        distances_dict: Dict[Tuple, List],
) -> Tuple[str]:
    """Find optimal segment from distances_dict computed by distance_from_segment.

    :param distances_dict: output of distance_from_segment.

    return key_min: name of the street that bounds the minimum distance segment
    """
    key_min = min(distances_dict.items(), key=itemgetter(1))[0]
    return key_min
