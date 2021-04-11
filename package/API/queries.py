"""Queries used with API."""


def query_city(
    rad: float,
    latitude: float,
    longitude: float,
):
    """."""
    overpass_query = f"""[out:json][timeout:800];
                        (node["place"="town"](around:{rad},{latitude},{longitude});
                        node["place"="city"](around:{rad},{latitude},{longitude}););
                        out body;
                        >;
                        out skel qt;"""
    return overpass_query


def query_street(
    rad: float,
    latitude: float,
    longitude: float,
):
    """."""
    overpass_query = f"""[out:json][timeout:800];
                    way
                      (around:{rad},{latitude},{longitude})
                      [name];
                    (._;>;);
                    out;"""
    return overpass_query


def query_ways(
    latitude: float,
    longitude: float,
) -> str:
    """."""
    overpass_query_get_ways = f"""[out:json][timeout:800];
                                    way
                                      (around:2,{latitude},{longitude})
                                      [name];
                                    (._;>;);
                                    out;"""
    return overpass_query_get_ways


def query_nodes(
    id_node: int,
) -> str:

    overpass_query_get_node = f"""[out:json][timeout:800];
                        node({id_node});
                        out;
                        """
    return overpass_query_get_node
