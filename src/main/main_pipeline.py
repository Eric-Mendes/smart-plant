from src.stages.extract.extract import ExtractSensores, ExtractTelemetry
from src.drivers.extract_thingsboard import DriversThingsBoard
from src.stages.load.load import LoadTransformedData
import time
import os

class MainPipeline:
    ''' Fluxo de execução do pipeline. '''
    @classmethod
    def run_pipeline(cls) -> None:
        ''' Execução do Fluxo de execução do pipeline'''

        #Extract 
        base_url = os.environ["thingsboard_url"]
        user = os.environ["thingsboard_user"]
        password = os.environ["thingsboard_pwd"]
        load = LoadTransformedData()

        thingsboard = None
        while True:
            try:
                if(thingsboard == None):
                    thingsboard = DriversThingsBoard(base_url, user, password)
                    continue
                else:
                    extract_sensores = ExtractSensores(thingsboard)
                    extract_telemetry = ExtractTelemetry(thingsboard)
            
                sensores_data = extract_sensores.prepareDevicesData()
                telemetry_data = extract_telemetry.prepareTelemetryData()

                load.load_sensors(sensores_data[0])
                load.load_telemetry(telemetry_data[0])
                time.sleep(1)
               
            except:
                thingsboard == None
                time.sleep(10)        

