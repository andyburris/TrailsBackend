from trailsbackend.local.db_repo import *
from trailsbackend.utils import id_sort

def get_all_areas(last_update):
    areas = db.areas.find({'last_update': {'$gte': last_update}})
    return sorted(list(areas), key=id_sort)

def get_all_area_ids():
    return list(map(lambda a: a['id'], get_all_areas()))

def get_areas_count():
    return db.areas.count_documents({})

def get_area(area_id):
    print("getting area " + str(area_id))
    return db.areas.find(where('id')==area_id)[0]

def clear_areas():
    db.areas.delete_many({})
