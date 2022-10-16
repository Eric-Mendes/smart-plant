import datetime
from .interfaces.extractor_thingsboard import ExtractorThingsBoardInterface
import datetime
import requests
import json


class DriversThingsBoard(ExtractorThingsBoardInterface):
    # @classmethod
    # def extract_thingsboard(cls) -> dict:

    #     """Adicionar"""
    #     response = requests.get(
    #         url="https://demo.thingsboard.io/api/plugins/telemetry/DEVICE/70a5e740-441b-11ed-a339-0708081d40ce/values/timeseries?keys=humidity,temperature",
    #         headers={
    #             "x-authorization": authorization,
    #             "content-type": "application/json",
    #         },
    #     )

    #     return response.json()
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

    #     return {
    #         "id": 1,
    #         "type":'temp',
    #         "value": 25,
    #         "unity": 'celsius',
    #         "located_at": 'Fabrica 01',
    #         "inserted_at":datetime.datetime.now(),
    #         "updated_at":datetime.datetime.now()
    # }





# ##Ajustar chaves 
# authorization = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJtYzg1NS5wcm9qZXRvLjVAZ21haWwuY29tIiwidXNlcklkIjoiMjFlZDM0NDAtMzMwNS0xMWVkLTg5YzItN2I4ZTljMzNmZDczIiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJpc3MiOiJ0aGluZ3Nib2FyZC5pbyIsImlhdCI6MTY2NTQyNDY1OSwiZXhwIjoxNjY3MjI0NjU5LCJmaXJzdE5hbWUiOiJTaXN0ZW1hIiwibGFzdE5hbWUiOiJOb3RpZmljYcOnw6NvIGRlIEV2ZW50b3MiLCJlbmFibGVkIjp0cnVlLCJwcml2YWN5UG9saWN5QWNjZXB0ZWQiOnRydWUsImlzUHVibGljIjpmYWxzZSwidGVuYW50SWQiOiIyMDlkZDBlMC0zMzA1LTExZWQtODljMi03YjhlOWMzM2ZkNzMiLCJjdXN0b21lcklkIjoiMTM4MTQwMDAtMWRkMi0xMWIyLTgwODAtODA4MDgwODA4MDgwIn0.ym0arShWcmtNJRiYL1XdZdcYvqH0gVxtj9Y3xbvaI-32YLjT_ktpfJgwKcFNBJGUwEa0re7ePhLKBCvvolGcag"

# # pylint disable
# class DriversThingsBoard(ExtractorThingsBoardInterface):
#     @classmethod
#     def extract_thingsboard(cls) -> dict:

#         """Adicionar"""
#         response = requests.get(
#             url="https://demo.thingsboard.io/api/plugins/telemetry/DEVICE/70a5e740-441b-11ed-a339-0708081d40ce/values/timeseries?keys=humidity,temperature",
#             headers={
#                 "x-authorization": authorization,
#                 "content-type": "application/json",
#             },
#         )

#         return response.json()

#     #     return {
#     #         "id": 1,
#     #         "type":'temp',
#     #         "value": 25,
#     #         "unity": 'celsius',
#     #         "located_at": 'Fabrica 01',
#     #         "inserted_at":datetime.datetime.now(),
#     #         "updated_at":datetime.datetime.now()
#     # }


# # 1. sensors <id, type, located_at, inserted_at, updated_at>;
# # 2. measurements <id, sensor_id, value, unit, inserted_at>
