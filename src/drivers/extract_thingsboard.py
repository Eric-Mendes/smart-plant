import requests

class DriversThingsBoard:
    token = None
    base_url = None

    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.token = self.getToken(user, password)
        
    def getToken(self, user, pwd):
        url = f"{self.base_url}/api/auth/login"

        payload = {
            "username": user,
            "password": pwd
        }

        response = requests.post(url = url, json = payload)

        token = response.json()["token"]

        return token

    def getDevices(self):
        url = f"{self.base_url}/api/tenant/devices?page=0&pageSize=9999"

        header = {
            "Authorization": f"Bearer {self.token}" 
        }

        response = requests.get(url = url, headers = header, timeout=20)

        devices = response.json()["data"]
        
        return devices

    def getTelemetry(self, device_id):

        url = f"{self.base_url}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
        
        header = {
            "Authorization": f"Bearer {self.token}" 
        }

        response = requests.get(url = url, headers = header, timeout=20)

        return response.json()
    
    
    def getKeys(self, device_id):
        url = f"{self.base_url}/api/plugins/telemetry/DEVICE/{device_id}/keys/timeseries"

        header = {
            "Authorization": f"Bearer {self.token}" 
        }

        response = requests.get(url = url, headers = header, timeout=20)

        return response.json()