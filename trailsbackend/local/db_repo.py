import pymongo

client = pymongo.MongoClient("mongodb+srv://trailsBackend:HmWMXwX0kNtxAmK8@trailsdatabase-b2ycz.mongodb.net/backend?retryWrites=true&w=majority")
db = client.backend