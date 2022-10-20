# from datetime import date
# from src.drivers.extractor_thingsboard import DriversThingsBoard
# from src.drivers.extractor_thingsboard import ExtractorThingsBoardInterface
# from src.stages.contracts.extract_contract import ExtractContract
# from src.errors.extract_error import ExtractError
import datetime

# from .extract import ExtractSensores
import json
import os
from pymongo import MongoClient


def test_extract():
    client = MongoClient('mongodb://db:27017/', username=os.environ["MONGO_INITDB_ROOT_USERNAME"], password=os.environ["MONGO_INITDB_ROOT_PASSWORD"])
    db = client.test_database
    collection = db.test_collection
    post = {"author": "Mike Love",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}
    # post_id = collection.insert_one(post).inserted_id
    # print(post_id)

    print(collection.find_one({"author": "Mike"}))
test_extract()