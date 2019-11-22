from trailsbackend.model.Update import Update
from trailsbackend.local.db_repo import *

def get_all_maps():
    return sorted(db.table('maps').all(), key=lambda a: a['id'])

def get_maps_count():
    return len(db.table('maps'))

def get_map(map_id):
    return db.table('maps').search(where('id')==map_id)

def get_all_map_updates(last_update):
    updates = db.table('updates').search((where('type')==Update.TYPE_MAP) & (where('time')>=last_update))
    return list(map(lambda u: get_map(u['object_key']), updates))

def clear_maps():
    db.table('maps').purge()

