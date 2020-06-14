class Thumbnail():
    width = 0
    height = 0
    url = ""

    def __init__(self, width, height, url):
        self.width = width
        self.height = height
        self.url = url

    def to_dict(self):
        thumbnail_dict = dict()
        thumbnail_dict.update({
            'width': self.width,
            'height': self.height,
            'url': self.url
        })
        return thumbnail_dict

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height and self.url == other.url

    def __hash__(self):
        return hash((self.width, self.height, self.url)) 

def dict_to_thumbnail(thumb_dict):
    return Thumbnail(thumb_dict['width'], thumb_dict['height'], thumb_dict['url'])