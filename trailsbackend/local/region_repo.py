from trailsbackend.model.Update import Update
from trailsbackend.local.db_repo import *

def get_all_regions():
    return db.table('regions').all()

def get_regions_count():
    return len(db.table('regions'))

def get_region(region_id):
    return db.table('regions').search(where('id')==region_id)[0]

def get_all_region_updates(last_update):
    updates = db.table('updates').search((where('type')==Update.TYPE_REGION) & (where('time')>=last_update))
    return list(map(lambda u: get_region(u['object_key']), updates))
    #return updates

def clear_regions():
    db.table('regions').purge()
