""" # thingsboard_etl
DAG responsável por periodicamente pegar os dados da plataforma do ThingsBoard e carregar no banco de dados.
"""

import os

from airflow import DAG
from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.utils.dates import days_ago

import requests
from pymongo import MongoClient

THINGSBOARD_URL = os.environ["THINGSBOARD_URL"]

def fetch_sensors():
    # TODO: pegar device_ids do banco
    return ["70a5e740-441b-11ed-a339-0708081d40ce"]


with DAG(
    dag_id="thingsboard_etl_1_0_1",
    description="DAG responsável por periodicamente pegar os dados da plataforma do ThingsBoard e carregar no banco de dados",
    schedule="0/5 * * * *",
    start_date=days_ago(1)
):  
    sensors = fetch_sensors()
    for sensor in sensors:
        @task(task_id=f"extract_data_from_{sensor}_sensor")
        def extract(device_id):
            device = Variable.get("devices", deserialize_json=True)[device_id]
            device_keys = ','.join(device["keys"])
            device_authorization_token = device["authorization_token"]

            thingsboard_endpoint = f"{THINGSBOARD_URL}/{device_id}/values/timeseries?keys={device_keys}"
            with requests.get(
                thingsboard_endpoint,
                headers={
                    "x-authorization": f"Bearer {device_authorization_token}",
                    "content-type": "application/json"
                }
            ) as response:
                response.raise_for_status()
                response_body = response.json()
                return {device_id: response_body}


        @task(task_id=f"transform_data_from_{sensor}_sensor")
        def transform(raw_data):
            print(raw_data)
            return raw_data

        @task(task_id=f"load_data_from_{sensor}_sensor")
        def load(transformed_data):
            db_client = MongoClient("mongodb://db:27017/")
            db = db_client.smart_factory_db
            measurements = db.measurements
            measurements.insert_one(transformed_data)

        
        load(transform(extract(sensor)))
