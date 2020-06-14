from trailsbackend.local.db_repo import *
from trailsbackend.utils import id_sort

def get_all_maps(last_update):
    areas = db.maps.find({'last_update': {'$gte': last_update}})
    return sorted(list(areas), key=id_sort)

def get_maps_count():
    return db.maps.count_documents({})

def get_map(map_id):
    return db.maps.find(where('id')==map_id)

def clear_maps():
    db.maps.delete_many({})

