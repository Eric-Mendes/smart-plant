from abc import ABC, abstractmethod

class ExtractorThingsBoardInterface(ABC):
    """Interface referente ao dados vindos do ThingsBoard"""

    # @classmethod
    # def extract_thingsboard(cls)-> dict:
    #     '''asd'''
    #     pass
    @classmethod
    def getToken(user, pwd) -> dict:
        ''' Interface referente a getToken'''
        pass
    @classmethod
    def getDevices(token)-> list:
        ''' Interface referente a getDevices'''
        pass
    @classmethod
    def getTelemetry(device_id, token) -> dict:
        ''' Interface referente a getTelemetry'''
        pass

