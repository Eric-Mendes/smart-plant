from datetime import date
from src.drivers.extract_thingsboard import DriversThingsBoard
from src.drivers.extract_thingsboard import ExtractorThingsBoardInterface
from src.stages.contracts.extract_contract import ExtractContract
from src.errors.extract_error import ExtractError

class ExtractSensores:
    ''' Extagios de extração '''

    def __init__(self,extractor_thingsboard:ExtractorThingsBoardInterface) -> None:
        '''Passando como paramentro o objeto extractor_excel'''
        self.extractor_thingsboard = extractor_thingsboard
    def extract_sensors(self)-> ExtractContract:
        '''Retorna um dicionario com dados brutos com seus respectivos data frames'''
        UNITY_TABLE  = {
        "temperature": "celcius - checar",
        "humidity": "g/m³ - checar",
        "distance": "m - checar"
    }
        try:
            extractor_thingsboard = DriversThingsBoard
            # Tirar credenciais no refinamento !!
            token = extractor_thingsboard.getToken("mc855.projeto.5@gmail.com", "vaX7Og1ehO74bFB")
            devices_ids = extractor_thingsboard.getDevices(token)
            data = []
            for device_id in devices_ids:
                result = extractor_thingsboard.getTelemetry(device_id, token)
                for key in result.keys():
                        data.append({
                            "sensor_id": device_id,
                            "type": key,
                            "value": result[key][0]["value"],
                            "unity": None,#UNITY_TABLE[key],
                            "located_at": None,
                            "inserted_at": result[key][0]["ts"],
                            "updated_at": result[key][0]["ts"]
                        })

            return ExtractContract(
                raw_information_content = data,
                extraction_date = date.today()
            )
        except Exception as exception:
            raise ExtractError(str(exception)) from exception
    ####
    extractor_thingsboard = DriversThingsBoard

