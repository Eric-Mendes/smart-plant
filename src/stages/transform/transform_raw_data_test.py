from src.stages.contracts.extract_contract import ExtractContract
from src.stages.extract.extract import ExtractSensores
from src.drivers.extractor_thingsboard import DriversThingsBoard
from src.stages.contracts.transform_contract import TransformContract
from .transform_raw_data import TransformRawData
import json

def test_transform():
    '''Testando transformação de dados '''
    extract_excel = DriversThingsBoard
    df_things_board = ExtractSensores(extract_excel)
    datas_things_board = df_things_board.extract()
    teste_contract  = TransformRawData()
    transfor_date_contract = teste_contract.transform(datas_things_board)
    print('-'*90)
    print(json.dumps(transfor_date_contract))

    assert isinstance(transfor_date_contract,TransformContract)