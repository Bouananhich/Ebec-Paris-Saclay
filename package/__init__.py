"""Init file of the package."""
import logging

from .API.get_nearest_city import get_nearest_city
from .API.get_nearest_street import get_nearest_street
from .API.get_ways_from_node import get_ways_from_node
from .logging_formatter import CustomFormatter
# pylint: disable=line-too-long
from .utils.utils import (conversion_list_dict, distance_from_segment,
                          find_optimal, get_road_sections, get_ways)

__all__ = ["get_nearest_city", "get_nearest_street", "get_ways_from_node", "get_ways",
           "get_road_sections", "distance_from_segment", "conversion_list_dict", "find_optimal"]


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)
