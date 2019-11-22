from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage

db = TinyDB('db.json')
#db = TinyDB(storage=MemoryStorage)