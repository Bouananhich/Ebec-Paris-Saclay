"""Get nearest street."""
import requests


def get_nearest_street(
    latitude: float,
    longitude: float
) -> str:
    n_iter = 0
    radplus = 100
    radmoins = 0
    overpass_url = "http://overpass-api.de/api/interpreter"
    rad = (radplus + radmoins) / 2
    overpass_query = query_street(
        rad=rad, latitude=latitude, longitude=longitude)
    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    data = response.json()
    ways = [x for x in data['elements'] if x['type'] == 'way']
    while len(ways) != 1:
        if n_iter == 10:
            n_iter = 0
            radplus += 1000
            rad = (radplus + radmoins) / 2
            overpass_query = query_street(
                rad=rad, latitude=latitude, longitude=longitude)
            response = requests.get(overpass_url,
                                    params={'data': overpass_query})
            data = response.json()
            ways = [x for x in data['elements'] if x['type'] == 'way']
        elif len(ways) == 0:
            n_iter += 1
            radmoins = rad
            rad = (radplus + radmoins) / 2
            overpass_query = query_street(
                rad=rad, latitude=latitude, longitude=longitude)
            response = requests.get(overpass_url,
                                    params={'data': overpass_query})
            data = response.json()
            ways = [x for x in data['elements'] if x['type'] == 'way']
        elif len(ways) >= 2:
            n_iter = 0
            radplus = rad
            rad = (radplus + radmoins) / 2
            overpass_query = query_street(
                rad=rad, latitude=latitude, longitude=longitude)
            response = requests.get(overpass_url,
                                    params={'data': overpass_query})
            data = response.json()
            ways = [x for x in data['elements'] if x['type'] == 'way']
    return ways[0]['tags']['name']


def query_street(
    rad: float,
    latitude: float,
    longitude: float,
):

    overpass_query = f"""[out:json];
                    way
                      (around:{rad},{latitude},{longitude})
                      [name];
                    (._;>;);
                    out;"""
    return overpass_query
