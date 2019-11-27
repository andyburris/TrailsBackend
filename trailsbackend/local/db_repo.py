from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage

db = TinyDB('/mnt/c/Users/andb3003/AppData/Local/Google/Cloud SDK/projects/trails-backend-3/trailsbackend/db.json')
#db = TinyDB(storage=MemoryStorage)