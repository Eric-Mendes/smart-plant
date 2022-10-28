# from datetime import date
# from src.drivers.extractor_thingsboard import DriversThingsBoard
# from src.drivers.extractor_thingsboard import ExtractorThingsBoardInterface
# from src.stages.contracts.extract_contract import ExtractContract
# from src.errors.extract_error import ExtractError
import datetime

# from .extract import ExtractSensores
import json
import os
from typing import Dict
from pymongo import MongoClient


class LoadTransformedData:
    def load(self, data: list | dict):
        """ Carrega dados no banco.

        ## Parâmetros
        - :param data: o dado a ser inserido no banco
        """
        client = MongoClient(
            'mongodb://db:27017/', 
            username=os.environ["MONGO_INITDB_ROOT_USERNAME"], 
            password=os.environ["MONGO_INITDB_ROOT_PASSWORD"]
        )
        db = client.smart_factory
        if isinstance(data, list):
            collection = db.measurements
            return collection.insert_many(data).inserted_ids
        else:
            collection = db.sensors
            return collection.insert_one(data).inserted_id
        