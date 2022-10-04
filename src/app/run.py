import random
from fastapi import FastAPI
from pydantic import BaseModel
import src.drivers.mocks.dash_mocker as web

# Criando aplicação
app = FastAPI()


# Rota Raiz
@app.get("/")
def root() -> dict:
    """Rota raiz"""
    return {"message": "Hello World"}  # Retornando um dicionário


@app.get("/users")
def listando_date_user() -> list:
    """Listando todos dados"""
    return web.create_user(1000)


#Kill
# @app.get("/history")
# def get_history(id:int,n_days:int) -> list:
#     """Retornando tempo para cada tipo de temperatura"""
#     print(id)
#     return web.get_history(27, 30, n_days=n_days)

#Kill
# @app.get("/timeLimites")
# def get_limit():
#     """Retornando tempo limite"""
#     return web.get_limit(20, 40)


@app.get("/sensorsInfo")
def get_sensors_info():
    return web.create_fake_sensors(10)

###################################################################################
#GET 
@app.get("/sensors/{sensor_id}")
def get_sensor(sensor_id:int):
    return web.sensor_builder(sensor_id)


#GET
@app.get("/sensors",tags=["sensors"],summary= 'Retorna n sensores')
def get_sensors(n_sensors:int):
    return [web.sensor_builder(i) for i in range(1, n_sensors+1)]

@app.get("/history")
def get_values(sensor_id:int, n_days:int):
    return web.build_temp_history(sensor_id, n_days)