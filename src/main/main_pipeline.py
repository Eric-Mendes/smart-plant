from datetime import datetime
from src.stages.extract.extract import ExtractSensores, ExtractTelemetry
from src.drivers.extract_thingsboard import DriversThingsBoard
from src.stages.load.load_aux import LoadTransformedData
import json 

class MainPipeline:
    ''' Fluxo de execução do pipeline. '''
    @classmethod
    def run_pipeline(cls) -> None:
        ''' Execução do Fluxo de execução do pipeline'''

        #Extract 
        base_url = "https://demo.thingsboard.io"
        user = "mc855.projeto.5@gmail.com"
        password = "vaX7Og1ehO74bFB"
        thingsboard = DriversThingsBoard(base_url, user, password)
        load = LoadTransformedData()

        while True:
            try:
                extract_sensores = ExtractSensores(thingsboard)
                extract_telemetry = ExtractTelemetry(thingsboard)
            except:
                print("ETL: Erro nas requests")
                continue

            sensores_data = extract_sensores.prepareDevicesData()
            telemetry_data = extract_telemetry.prepareTelemetryData()

            load.load_sensors(sensores_data[0])
            load.load_telemetry(telemetry_data[0])
        

