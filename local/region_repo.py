from local.db_repo import *
from utils import id_sort, remove_underscore

def get_all_regions(last_update):
    regions = db.regions.find({'last_update': {'$gte': last_update}})
    return sorted(list(map(remove_underscore, regions)), key=id_sort)

def get_regions_count():
    return db.regions.count_documents({})

def get_region(region_id):
    return db.regions.find({'_id': region_id})[0]

def clear_regions():
    db.regions.delete_many({})
