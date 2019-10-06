
import datetime
from tinydb import TinyDB, where
UPDATE_TYPE_REGION = 0
UPDATE_TYPE_AREA = 1
UPDATE_TYPE_MAP = 2

db = TinyDB('db.json')

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
    
    def to_dict(self):
        region_dict = dict
        region_dict.update({
            'id': self.id,
            'name': self.name,
            'map_count': self.map_count,
            'parent_id': self.parent_id,
        })
        return region_dict

def dict_to_region(area_dict):
    return Region(area_dict['id'], area_dict['name'], area_dict['map_count'], area_dict['parent_id'])

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
    
    def to_dict(self):
        area_dict = dict()
        area_dict.update({
            'id': self.id,
            'name': self.name,
            'maps': self.maps,
            'info': self.info,
            'parent_ids': self.parent_ids,
        })
        return entity

def dict_to_area(area_dict):
    return Area(area_dict['id'], area_dict['name'], area_dict['map_count'], area_dict['parent_id'])

class Update():
    time = datetime.datetime.now
    type = -1
    object_key = -1
    
    def __init__(self, type, object_key):
        self.type = type
        self.object_key = object_key

    def to_dict(self):
        update_dict = dict()
        update_dict.update({
            'time': self.time,
            'type': self.type,
            'object_key': self.object_key,
        })
        return update_dict

def dict_to_update(update_dict):
    return Update(update_dict['time'], update_dict['type'], update_dict['object_key'])