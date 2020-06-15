import datetime
epoch = datetime.datetime.utcfromtimestamp(0)

class Area():
    id = -1
    name = ""
    maps = []
    info = dict()
    parent_ids = []
    last_update = -1

    def __init__(self, id, name, maps, info, parent_ids):
        self.id = id
        self.name = name
        self.maps = maps
        self.info = info
        self.parent_ids = parent_ids

    def __str__(self):
        return "Area: " + self.name + " (" + str(self.id) + ") \n" + "maps: " + str(self.maps) + "\n" + "info: " + str(self.info) + "\n" + "parents: " + str(self.parent_ids)
    
    def to_dict(self):
        area_dict = dict()
        millis_time = (self.last_update - epoch).total_seconds() * 1000
        area_dict.update({
            '_id': self.id,
            'name': self.name,
            'maps': self.maps,
            'info': self.info,
            'parent_ids': self.parent_ids,
            'last_update': millis_time,
        })
        return area_dict

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.maps == other.maps and self.info == other.info and self.parent_ids == other.parent_ids

    def __hash__(self):
        return hash((self.id, self.name, self.maps, self.info, self.parent_ids))

def dict_to_area(area_dict):
    return Area(area_dict['_id'], area_dict['name'], area_dict['maps'], area_dict['info'], area_dict['parent_ids'])