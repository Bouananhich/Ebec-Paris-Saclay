"""Get nearest city."""
import requests

def get_nearest_city(
    latitude: float,
    longitude: float,
) -> str:
    """blabla"""
    n_iter = 0
    radplus = 10000
    radmoins = 0
    rad = (radplus + radmoins) / 2
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = query_city(
        rad=rad, latitude=latitude, longitude=longitude)
    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    data = response.json()
    while len(data['elements']) != 1:
        if n_iter == 10:
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


def query_city(
    rad: float,
    latitude: float,
    longitude: float,
):
    overpass_query = f"""[out:json][timeout:25];
                        (node["place"="town"](around:{rad},{latitude},{longitude});
                        node["place"="city"](around:{rad},{latitude},{longitude}););
                        out body;
                        >;
                        out skel qt;"""
    return overpass_query
