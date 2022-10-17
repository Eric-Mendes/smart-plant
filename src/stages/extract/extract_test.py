from datetime import date
from src.drivers.extractor_thingsboard import DriversThingsBoard
from src.drivers.extractor_thingsboard import ExtractorThingsBoardInterface
from src.stages.contracts.extract_contract import ExtractContract
from src.errors.extract_error import ExtractError

from .extract import ExtractSensores
import json

def test_extract():
    '''  dsdefg'''
    extract_excel = ExtractSensores
    df_thinsg_board = ExtractSensores(extract_excel)
    datas_thinsg_board = df_thinsg_board.extract()
    #print()
    print(json.dumps(datas_thinsg_board[0]))
    
    #print(datas_thinsg_board)
    #assert isinstance(datas_thinsg_board,ExtractContract)


