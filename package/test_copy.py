import logging

from .utils.utils import (conversion_list_dict, distance_from_segment,
                          find_optimal, get_road_sections, get_ways,get_order_in_segment)

#from  .API.get_nearest_city import (get_nearest_city)
#from  .API.get_nearest_street import (get_nearest_street)

log_level = logging.INFO
logging.getLogger("package").setLevel(log_level)



coords = [(48.89535,2.24697),(48.89529,2.24705),(48.89518,2.2472),(48.89394122, 2.247959188)]
result={}
roads_dict={}
for coord in coords:
    ways, name = get_ways(*coord)
    roads = get_road_sections(intersection_list=ways, road_name=name)
    roads_dict.update(conversion_list_dict(roads))
    dict_distances = distance_from_segment(coord, roads_dict)
    troncon = find_optimal(dict_distances)
    if troncon in result:
        result[troncon].append(coord)
    else:
        result[troncon]=[]
        result[troncon].append(coord)

city={}
street={}
Resultat_inter={}
for troncon in result:
    coords=result[troncon]
    if len(coords)==1:
        test={coords[0]:1}
    noeuds_troncon=roads_dict[troncon]
    section=[troncon[0],troncon[1],noeuds_troncon[0],noeuds_troncon[1]]
    test=get_order_in_segment(coords,section)
    #city[troncon]=get_nearest_city(coords[0][0],coords[0][1])
    #street[troncon]=get_nearest_street(coords[0][0],coords[0][1])
    Resultat_inter[troncon]=test
    #print(test)

Liste_resultat=[]
for troncon in result:
    coords=result[troncon]
    for coord in coords:
        Liste_resultat.append([coord,"street[troncon]",troncon[0],troncon[1],Resultat_inter[troncon][coord],"city[troncon]"])

print(Liste_resultat)
#df=pd.dataframe(Liste_resultat)





#coord = 48.89394122, 2.247959188
