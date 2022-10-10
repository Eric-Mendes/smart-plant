from datetime import date
from src.drivers.extractor_thingsboard import DriversThingsBoard
from src.drivers.extractor_thingsboard import ExtractorThingsBoardInterface
from src.stages.contracts.extract_contract import ExtractContract
from src.errors.extract_error import ExtractError

from .extract import ExtractSensores


def test_extract():
    '''  dsdefg'''
    extract_excel = ExtractSensores
    df_allure = ExtractSensores(extract_excel)
    datas_allure = df_allure.extract()
    #print(datas_allure)
    
    #print(datas_allure)
    #assert isinstance(datas_allure,ExtractContract)


