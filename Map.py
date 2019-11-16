from Thumbnail import *

class Map():
    id = -1
    year = 1970
    thumbnails = []
    image_url = ""
    parent_id = -1

    def __init__(self, id, year, thumbnails, image_url, parent_id):
        self.id = id
        self.year = year
        self.thumbnails = thumbnails
        self.image_url = image_url
        self.parent_id = parent_id

    def to_dict(self):
        map_dict = dict()
        map_dict.update({
            'id': self.id,
            'year': self.year,
            'thumbnails': list(map(lambda t: t.to_dict(), self.thumbnails)),
            'image_url': self.image_url,
            'parent_id': self.parent_id,
        })
        return map_dict

def dict_to_map(map_dict):
    return Map(map_dict['id'], map_dict['year'], list(map(dict_to_thumbnail, map_dict['thumbnails'])), map_dict['image_url'], map_dict['parent_id'])