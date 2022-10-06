from src.stages.contracts.extract_contract import ExtractContract
from src.stages.extract.extract import ExtractSensores
from src.drivers.extractor_thingsboard import DriversThingsBoard
from src.stages.contracts.transform_contract import TransformContract
from .transform_raw_data import TransformRawData


def test_transform():
    '''hbfgkjghjohdgjlkdhgjldhgjlk'''
    extract_excel = DriversThingsBoard
    df_allure = ExtractSensores(extract_excel)
    datas_allure = df_allure.extract()
    teste_contract  = TransformRawData()
    transfor_date_contract = teste_contract.transform(datas_allure)
    #print(transfor_date_contract)

    assert isinstance(transfor_date_contract,TransformContract)