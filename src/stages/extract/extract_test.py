from datetime import date
from src.drivers.extract_thingsboard import DriversThingsBoard
from .extract import ExtractSensores
from .extract import ExtractTelemetry
import json

def test_extract():
    '''  Testando etapa de extração'''
    base_url = "https://demo.thingsboard.io"
    user = "mc855.projeto.5@gmail.com"
    password = "vaX7Og1ehO74bFB"
    thingsboard = DriversThingsBoard(base_url, user, password)
    extract_sensores = ExtractSensores(thingsboard)
    extract_telemetry = ExtractTelemetry(thingsboard)
    sensores_data = extract_sensores.prepareDevicesData()
    extract_telemetry = extract_telemetry.prepareTelemetryData()
    
    print(json.dumps(sensores_data[0] ))
    print()
    print(json.dumps(extract_telemetry[0]))



