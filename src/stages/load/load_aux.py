
import datetime
import os
from pymongo import MongoClient
import os

class LoadTransformedData:
    def __init__(self):
        self.client =  MongoClient(
        'mongodb://db:27017/', 
        username='root', 
        password='example'
        )
        
    def load_sensors(self, data: list):
        db = self.client.smart_factory
        collection = db.sensors
        list_sensor = []
        db_data = collection.find({})
        ids = [data["sensor_id"] for data in db_data]
        for sensor in data:
            if(sensor['sensor_id'] not in ids):
                list_sensor.append(sensor)

        if(len(list_sensor) > 0):
            collection.insert_many(list_sensor)

    def load_telemetry(self, data: list):
        db = self.client.smart_factory
        collection = db.telemetry
        list_telemetry = []
        db_data = collection.find({})
        ids = [data["telemetry_id"] for data in db_data]
        for telemetry in data:
            if(telemetry['telemetry_id'] not in ids):
                list_telemetry.append(telemetry)

        
        if(len(list_telemetry) > 0):
            collection.insert_many(list_telemetry)
