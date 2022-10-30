import pymongo
from .models import *

class MongoConnection:
    def __init__(self):
        self.client =  pymongo.MongoClient(
            'mongodb://db:27017/', 
            username='root', 
            password='example'
        )

    def get_sensors_list(self):
        db = self.client.smart_factory
        sensors_collection  = db.sensors

        return list(sensors_collection.find({}, {'_id': False}))

    def get_telemetry_list(self):
        db = self.client.smart_factory
        telemetry_collection  = db.telemetry

        return list(telemetry_collection.find({}, {'_id': False}))
    
    def get_sensor(self, sensor_id):
        db = self.client.smart_factory
        sensors_collection  = db.sensors

        return list(sensors_collection.find({"sensor_id": sensor_id}, {'_id': False}))
    
    def get_sensor_telemetry(self, sensor_id):
        db = self.client.smart_factory
        sensors_collection  = db.telemetry

        return list(sensors_collection.find({"sensor_id": sensor_id}, {'_id': False}))
    
    def patch_sensor(self, sensor_id, data):
        my_dict = data.__dict__
        my_dict = dict([(key, value) for key, value in list(my_dict.items()) if value != False])

        db = self.client.smart_factory
        sensors_collection  = db.sensors

        if("info" in my_dict.keys()):
            my_info = [a_dict.__dict__ for a_dict in my_dict["info"]]

            sensor = list(sensors_collection.find({"sensor_id": sensor_id}, {'_id': False}))[0]
            type_list = [info["type"] for info in sensor["info"]]

            for info in my_info:
                if(info["type"] in type_list):
                    pos = type_list.index(info["type"])
                    if(info["bottom_limit"] != False):
                        my_dict[f"info.{pos}.bottom_limit"] = info["bottom_limit"]
                    if(info["upper_limit"] != False):
                        my_dict[f"info.{pos}.upper_limit"] = info["upper_limit"]
            
            del my_dict["info"]

        sensors_collection.update_one({"sensor_id": sensor_id}, {"$set": my_dict})
