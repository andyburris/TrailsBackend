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
    region_ids = list(map(lambda u: u['object_key'], updates))
    all_regions = db.table('regions').all()
    return list(filter(lambda a: a['id'] in region_ids, all_regions))

def clear_regions():
    db.table('regions').purge()
