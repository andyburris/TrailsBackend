import pymongo
import os

password = os.environ['TRAILS_MONGODB_PASSWORD']
client = pymongo.MongoClient("mongodb+srv://trailsBackend:" + password + "@trailsdatabase-b2ycz.mongodb.net/backend?retryWrites=true&w=majority")
db = client.backend