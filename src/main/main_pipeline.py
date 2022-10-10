from datetime import datetime
from src.stages.extract.extract import ExtractSensores
from src.drivers.extractor_thingsboard import DriversThingsBoard
from src.stages.transform.transform_raw_data import TransformRawData


class MainPipeline:
    ''' Colocar doctring'''
    @classmethod
    def run_pipeline(cls) -> None:
        ''' Colocar doctring'''
        inicio = datetime.now()
        print(f"Inicio: {inicio}")
        
        df_allure = ExtractSensores(DriversThingsBoard)
        datas_allure = df_allure.extract()

        teste_contract  = TransformRawData()
        transform_data = teste_contract.transform(datas_allure)

        print(transform_data)

        fim = datetime.now()
        print(f"Fim: {fim}")
        print(f"Diferenca de data {fim-inicio} ")
