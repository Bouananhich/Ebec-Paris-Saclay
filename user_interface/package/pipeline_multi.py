import logging

from .utils.utils import (conversion_list_dict, distance_from_segment,
                          find_optimal, get_road_sections, get_ways,get_order_in_segment,merge_sections)

#from  .API.get_nearest_city import (get_nearest_city)
#from  .API.get_nearest_street import (get_nearest_street)

log_level = logging.INFO
logging.getLogger("package").setLevel(log_level)

import pandas as pd

def pipeline_multi(list_input):
    resultat=[]
    for coords in list_input:
        
        result={}
        roads_dict={}

        for coord in coords:
            ways, name = get_ways(*coord)
            roads =get_road_sections(intersection_list=ways, road_name=name)
            roads_dict.update(conversion_list_dict(roads))
            dict_distances = distance_from_segment(coord, roads_dict)
            troncon = find_optimal(dict_distances)
            if troncon in result:
                result[troncon].append(coord)
            else:
                result[troncon]=[]
                result[troncon].append(coord)

        liste_inter=[]
        for troncon in result:
            section=[*troncon,*roads_dict[troncon]]
            liste_inter.append(section)
        
        resultat_coords=merge_sections(liste_inter[0],liste_inter[1],roads)
        resultat.append(resultat_coords)

    df=pd.DataFrame(resultat)

    return df
