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

        db_data = collection.find({})

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

        list_sensor = [sensor for sensor in data if sensor["sensor_id"] not in ids_in_db]
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