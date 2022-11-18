import datetime
from .interfaces.extractor_thingsboard import ExtractorThingsBoardInterface
import datetime
import requests
import json


class DriversThingsBoard(ExtractorThingsBoardInterface):


    @classmethod
    def getToken(cls,user, pwd) -> dict:
        url = "https://demo.thingsboard.io/api/auth/login"

        payload = {
            "username": user,
            "password": pwd
        }

        response = requests.post(url = url, json = payload)

        token = response.json()["token"]

        return token
    @classmethod
    def getDevices(cls,token)-> list:
        url = f"https://demo.thingsboard.io/api/tenant/devices?page=0&pageSize=9999"

        header = {
            "Authorization": f"Bearer {token}" 
        }

        response = requests.get(url = url, headers = header)

        devices = response.json()["data"]

        ids = [device["id"]["id"] for device in devices]
        
        return ids
    @classmethod
    def getTelemetry(cls,device_id, token) -> dict:

        url = f"https://demo.thingsboard.io/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
        
        header = {
            "Authorization": f"Bearer {token}" 
        }

        response = requests.get(url = url, headers = header)

        return response.json()

    