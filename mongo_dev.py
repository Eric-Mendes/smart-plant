from logging import root
import pymongo
import os
import json

client = pymongo.MongoClient(
        'mongodb://localhost:27017/', 
        username='root', 
        password='example'
)
# Para deletar os dados do banco
db = client.smart_factory
collection = db.sensors
collection.delete_many({})

collection = db.telemetry
collection.delete_many({})


print(list(collection.find({}, {'_id': False})))

