from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage

db = TinyDB('</path/to/project/directory>' + '/trailsbackend/db.json')
#db = TinyDB(storage=MemoryStorage)