
import datetime
from google.cloud import firestore
UPDATE_TYPE_REGION = 0
UPDATE_TYPE_AREA = 1
UPDATE_TYPE_MAP = 2

client = firestore.Client()

class Region():
    id = -1
    name = ""
    map_count = -1
    parent_id = -1

    def __init__(self, id, name, map_count, parent_id):
        self.id = id
        self.name = name
        self.map_count = map_count
        self.parent_id = parent_id

    def __eq__(self, other):
        if not isinstance(other, Region):
            return NotImplemented
        return self.id == other.id and self.name == other.name and self.map_count == other.map_count and self.parent_id == other.parent_id
    
    def to_entity(self):
        entity = client.collection(u'Region').document(str(self.id))
        entity.set({
            'id': self.id,
            'name': self.name,
            'map_count': self.map_count,
            'parent_id': self.parent_id,
        })
        return entity

def entity_to_region(entity):
    return Region(entity.id, entity['name'], entity['map_count'], entity['parent_id'])

class Area():
    id = -1
    name = ""
    maps = []
    info = dict()
    parent_ids = []

    def __init__(self, id, name, maps, info, parent_ids):
        self.id = id
        self.name = name
        self.maps = maps
        self.info = info
        self.parent_ids = parent_ids

    def __eq__(self, other):
        if not isinstance(other, Region):
            return NotImplemented
        return self.id == other.id and self.name == other.name and self.maps == other.maps and self.info == other.info and self.parent_ids == other.parent_ids
    
    def to_entity(self):
        entity = client.collection('Area').document(str(self.id))
        entity.set({
            'id': self.id,
            'name': self.name,
            'maps': self.maps,
            'info': self.info,
            'parent_ids': self.parent_ids,
        })
        return entity

def entity_to_region(entity):
    return Region(entity.id, entity['name'], entity['map_count'], entity['parent_id'])

class Update():
    time = datetime.datetime.now
    type = -1
    object_key = -1
    
    def __init__(self, type, object_key):
        self.type = type
        self.object_key = object_key

    def to_entity(self):
        key = client.key('Update')
        entity = client.collection('Update').document()
        entity.update({
            'time': self.time,
            'type': self.type,
            'object_key': self.object_key,
        })
        return entity

def entity_to_update(entity):
    return Update(entity['time'], entity['type'], entity['object_key'])