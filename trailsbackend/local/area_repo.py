from trailsbackend.model.Update import Update
from trailsbackend.local.db_repo import *

def get_all_areas():
    return sorted(db.table('areas').all(), key=lambda a: a['id'])

def get_all_area_ids():
    return list(map(lambda a: a['id'], get_all_areas()))

def get_areas_count():
    return len(db.table('areas'))

def get_area(area_id):
    print("getting area " + str(area_id))
    return db.table('areas').search(where('id')==area_id)[0]

def get_all_area_updates(last_update):
    updates = db.table('updates').search((where('type')==Update.TYPE_AREA) & (where('time')>=last_update))
    area_ids = list(map(lambda u: u['object_key'], updates))
    all_areas = db.table('areas').all()
    return list(filter(lambda a: a['id'] in area_ids, all_areas))

def clear_areas():
    db.table('areas').purge()
