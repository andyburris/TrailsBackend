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

    def __str__(self):
        return "Area: " + self.name + " (" + str(self.id) + ") \n" + "maps: " + str(self.maps) + "\n" + "info: " + str(self.info) + "\n" + "parents: " + str(self.parent_ids)
    
    def to_dict(self):
        area_dict = dict()
        area_dict.update({
            'id': self.id,
            'name': self.name,
            'maps': self.maps,
            'info': self.info,
            'parent_ids': self.parent_ids,
        })
        return area_dict

def dict_to_area(area_dict):
    return Area(area_dict['id'], area_dict['name'], area_dict['map_count'], area_dict['info'], area_dict['parent_id'])