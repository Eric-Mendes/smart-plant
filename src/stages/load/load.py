from pymongo import MongoClient

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

        db_data = list(collection.find({}))

        ids_in_db = [my_data["sensor_id"] for my_data in db_data]
        ids_from_tb = [my_data["sensor_id"] for my_data in data]

        remove_ids = list(set(ids_in_db) - set(ids_from_tb))
        if(len(remove_ids) > 0):
            collection.delete_many({
                "sensor_id": {
                    "$in": remove_ids
                }
            })

            db.telemetry.delete_many({
                "sensor_id": {
                    "$in": remove_ids
                }
            })

        sensors_to_insert = [sensor for sensor in data if sensor["sensor_id"] not in ids_in_db]
        if(len(sensors_to_insert) > 0):
            collection.insert_many(sensors_to_insert)
        
        sensors_from_db_in_tb= {
            sensor["sensor_id"]: sensor
            for sensor in db_data
            if sensor["sensor_id"] in ids_from_tb
        }

        for sensor_in_tb in data:
            if(sensor_in_tb["sensor_id"] in sensors_from_db_in_tb.keys()):
                sensor_in_db = sensors_from_db_in_tb[sensor_in_tb["sensor_id"]]

                metrics_db = [(info["type"],info["unity"]) for info in sensor_in_db["info"]]
                metrics_tb = [(info["type"],info["unity"]) for info in sensor_in_tb["info"]]

                metrics_to_add = list(set(metrics_tb) - set(metrics_db))
                
                new_info = [
                    info 
                    for info in sensor_in_tb["info"] 
                    if (info["type"],info["unity"]) in metrics_to_add 
                ]

                collection.update_one({"sensor_id": sensor_in_tb["sensor_id"]}, {"$push": {"info": {"$each": new_info}}})

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

