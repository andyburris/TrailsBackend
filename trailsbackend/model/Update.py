import datetime

class Update():
    time = datetime.datetime.now()
    object_key = -1

    TYPE_REGION = 0
    TYPE_AREA = 1
    TYPE_MAP = 2
    
    def __init__(self, type, object_key):
        self.type = type
        self.object_key = object_key

    def to_dict(self):

        epoch = datetime.datetime.utcfromtimestamp(0)
        millis_time = (self.time - epoch).total_seconds() * 1000

        update_dict = dict()
        update_dict.update({
            'time': millis_time,
            'type': self.type,
            'object_key': self.object_key,
        })
        return update_dict

def dict_to_update(update_dict):
    return Update(update_dict['time'], update_dict['type'], update_dict['object_key'])