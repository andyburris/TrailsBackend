from .Thumbnail import *
import datetime
epoch = datetime.datetime.utcfromtimestamp(0)

class Map():
    id = -1
    year = 1970
    thumbnails = []
    image_url = ""
    parent_id = -1    
    last_update = -1

    def __init__(self, id, year, thumbnails, image_url, parent_id):
        self.id = id
        self.year = year
        self.thumbnails = thumbnails
        self.image_url = image_url
        self.parent_id = parent_id

    def to_dict(self):
        map_dict = dict()
        millis_time = (self.last_update - epoch).total_seconds() * 1000
        map_dict.update({
            '_id': self.id,
            'year': self.year,
            'thumbnails': list(map(lambda t: t.to_dict(), self.thumbnails)),
            'image_url': self.image_url,
            'parent_id': self.parent_id,
            'last_update': millis_time,
        })
        return map_dict
    
    def __eq__(self, other):
        return self.id == other.id and self.year == other.year and self.thumbnails == other.thumbnails and self.image_url == other.image_url and self.parent_id == other.parent_id

    def __hash__(self):
        return hash((self.id, self.year, self.thumbnails, self.image_url, self.parent_id))

def dict_to_map(map_dict):
    return Map(map_dict['_id'], map_dict['year'], list(map(dict_to_thumbnail, map_dict['thumbnails'])), map_dict['image_url'], map_dict['parent_id'])