class Region():
    id = -1
    name = ""
    child_regions = []
    child_areas = []
    map_count = -1
    parent_id = -1

    def __init__(self, id, name, child_regions, child_areas, map_count, parent_id):
        self.id = id
        self.name = name
        self.child_regions = child_regions
        self.child_areas = child_areas
        self.map_count = map_count
        self.parent_id = parent_id

    def __eq__(self, other):
        if not isinstance(other, Region):
            return NotImplemented
        return self.id == other.id and self.name == other.name and self.map_count == other.map_count and self.parent_id == other.parent_id
    
    def to_dict(self):
        region_dict = dict()
        region_dict.update({
            'id': self.id,
            'name': self.name,
            'child_regions': self.child_regions,
            'child_areas': self.child_areas,
            'map_count': self.map_count,
            'parent_id': self.parent_id,
        })
        return region_dict

def dict_to_region(region_dict):
    return Region(region_dict['id'], region_dict['name'], region_dict['child_regions'], region_dict['child_areas'], region_dict['map_count'], region_dict['parent_id'])
