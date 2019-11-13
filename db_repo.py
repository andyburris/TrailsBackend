from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage
from google.cloud import storage

db = TinyDB('db.json')
#db = TinyDB(storage=MemoryStorage)
storage_client = storage.Client()
bucket = storage_client.get_bucket("trailsbackend-254417.appspot.com")