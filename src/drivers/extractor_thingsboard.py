import datetime
from .interfaces.extractor_thingsboard import ExtractorThingsBoardInterface
import  datetime
import requests


#pylint disable 
class DriversThingsBoard(ExtractorThingsBoardInterface):
    @classmethod
    def extract_thingsboard(cls)-> dict:

        ''' Adicionar '''
        return {
            "id": 1,
            "type":'temp',
            "value": 25,
            "unity": 'celsius',
            "located_at": 'Fabrica 01',
            "inserted_at":datetime.datetime.now(),
            "updated_at":datetime.datetime.now()
    }


#1. sensors <id, type, located_at, inserted_at, updated_at>;
#2. measurements <id, sensor_id, value, unit, inserted_at>




