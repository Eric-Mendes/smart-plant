from datetime import date
from src.drivers.extractor_thingsboard import DriversThingsBoard
from src.drivers.extractor_thingsboard import ExtractorThingsBoardInterface
from src.stages.contracts.extract_contract import ExtractContract
from src.errors.extract_error import ExtractError



class ExtractSensores:
    ''' Extagios de extração '''
    def __init__(self,extractor_excel:ExtractorThingsBoardInterface) -> None:
        '''Passando como paramentro o objeto extractor_excel'''
        self.extractor_excel = extractor_excel
    def extract(self)-> ExtractContract:
        '''Retorna um dicionario com dados brutos com seus respectivos data frames'''
        try:
            extractor_pandas = DriversThingsBoard
            return ExtractContract(
                raw_information_content = extractor_pandas.extract_thingsboard(),
                extraction_date = date.today()
            )
        except Exception as exception:
            raise ExtractError(str(exception)) from exception
