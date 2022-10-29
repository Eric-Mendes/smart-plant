from datetime import datetime
from src.stages.extract.extract import ExtractSensores
from src.drivers.extractor_thingsboard import DriversThingsBoard
from src.stages.load.load import LoadTransformedData
from src.stages.transform.transform_raw_data import TransformRawData


class MainPipeline:
    ''' Colocar doctring'''
    @classmethod
    def run_pipeline(cls) -> None:
        ''' Colocar doctring'''
        # inicio = datetime.now()
        # print(f"Inicio: {inicio}")
        
        df_things_board = ExtractSensores(DriversThingsBoard)
        datas_things_board = df_things_board.extract()

        teste_contract  = TransformRawData()
        transform_data = teste_contract.transform(datas_things_board)
        #print(transform_data[0])
        load = LoadTransformedData()
        load_result = load.load(transform_data[0])
        
        # fim = datetime.now()
        # print(f"Fim: {fim}")
        # print(f"Diferenca de data {fim-inicio} ")
