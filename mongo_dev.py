from logging import root
import pymongo
import os
import json

client = pymongo.MongoClient(
        'mongodb://localhost:27017/', 
        username='root', 
        password='example'
        )
db = client.smart_factory
collection = db.sensors
collection.delete_many({})

collection = db.telemetry
collection.delete_many({})

#collection.insert_one({'Name':'pini','idade':8000})


print(list(collection.find({}, {'_id': False})))