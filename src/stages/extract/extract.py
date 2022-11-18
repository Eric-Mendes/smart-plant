from datetime import date
from src.drivers.extract_thingsboard import DriversThingsBoard
from src.stages.contracts.extract_contract import ExtractContract
from src.errors.extract_error import ExtractError
import json 
import hashlib

class ExtractSensores:
    ''' Extagios de extração '''

    def __init__(self,extractor_thingsboard:DriversThingsBoard) -> None:
        '''Passando como paramentro o objeto extractor_excel'''
        self.extractor_thingsboard = extractor_thingsboard
    def prepareDevicesData(self):

        try:
            devices = self.extractor_thingsboard.getDevices()
            data = []
            for device in devices:
                data.append({
                    "sensor_id": device["id"]["id"],
                    "name": device["name"],
                    "located_at": None,
                    "info":[
                        {
                            "type": key.split("_")[0],
                            "unity": key.split("_")[-1],
                            "upper_limit":None,
                            "bottom_limit":None

                        } for key in self.extractor_thingsboard.getKeys(device["id"]["id"])
                    ],
                    'groups':["Admin"]
                    
                })
            return ExtractContract(
                raw_information_content = data,
                extraction_date = date.today()
            )
        except Exception as exception:
            raise ExtractError(str(exception)) from exception

class ExtractTelemetry:
    ''' Extagios de extração '''
    def __init__(self,extractor_thingsboard:DriversThingsBoard) -> None:
        '''Passando como paramentro o objeto extractor_excel'''
        self.extractor_thingsboard = extractor_thingsboard
    def prepareTelemetryData(self) -> list:

        try:
            devices = self.extractor_thingsboard.getDevices()
            ids = [device["id"]["id"] for device in devices]
            data = []
            for device_id in ids:
                result = self.extractor_thingsboard.getTelemetry(device_id)

                for key in result.keys():
                    my_type = key.split("_")[0]
                    unity = key.split("_")[-1]

                    my_data = {
                            "sensor_id": device_id,
                            "type": my_type,
                            "value": result[key][0]["value"],
                            "unity": unity,
                            "inserted_at": result[key][0]["ts"]
                    }

                    my_json = json.dumps(my_data, sort_keys=True)
                    my_hash = hashlib.md5(my_json.encode("utf-8")).hexdigest()

                    data.append({
                        "telemetry_id":my_hash,
                        **my_data
                    })

            return ExtractContract(
                raw_information_content = data,
                extraction_date = date.today()
            )
        except Exception as exception:
            raise ExtractError(str(exception)) from exception
