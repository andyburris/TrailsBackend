from local.db_repo import *
from utils import id_sort, remove_underscore

def get_all_maps(last_update):
    maps = db.maps.find({'last_update': {'$gte': last_update}})
    return sorted(list(map(remove_underscore, maps)), key=id_sort)

def get_maps_count():
    return db.maps.count_documents({})

def get_map(map_id):
    return db.maps.find({'_id': map_id})[0]

def clear_maps():
    db.maps.delete_many({})

