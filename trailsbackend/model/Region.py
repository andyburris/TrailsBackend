import datetime
epoch = datetime.datetime.utcfromtimestamp(0)

class Region():
    id = -1
    name = ""
    child_regions = []
    child_areas = []
    map_count = -1
    parent_id = -1
    last_update = -1

    def __init__(self, id, name, child_regions, child_areas, map_count, parent_id):
        self.id = id
        self.name = name
        self.child_regions = child_regions
        self.child_areas = child_areas
        self.map_count = map_count
        self.parent_id = parent_id
    
    def to_dict(self):
        region_dict = dict()
        millis_time = (self.last_update - epoch).total_seconds() * 1000
        region_dict.update({
            '_id': self.id,
            'name': self.name,
            'child_regions': self.child_regions,
            'child_areas': self.child_areas,
            'map_count': self.map_count,
            'parent_id': self.parent_id,
            'last_update': millis_time,
        })
        return region_dict
    
    def __str__(self):
        return "Region(" + self.name + "id: " + str(self.id) + "\nname: " + str(self.name) + "\nchild_regions: " + str(self.child_regions) + "\nchild_areas: " + str(self.child_areas) + "\nmap_count: " + str(self.map_count) + "\nparent_id: " + str(self.parent_id) + ")"

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.child_regions == other.child_regions and self.child_areas == other.child_areas and self.map_count == other.map_count and self.parent_id == other.parent_id

    def __hash__(self):
        return hash((self.id, self.name, self.child_regions, self.child_areas, self.map_count, self.parent_id))

def dict_to_region(region_dict):
    return Region(region_dict['_id'], region_dict['name'], region_dict['child_regions'], region_dict['child_areas'], region_dict['map_count'], region_dict['parent_id'])
