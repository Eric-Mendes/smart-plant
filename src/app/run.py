from functools import lru_cache

from fastapi import FastAPI, status, Response, Depends

import src.drivers.interfaces.keycloak_auth as auth
import src.drivers.mocks.dash_mocker as web
from src.drivers.interfaces.config import Settings


# Criando aplicação
app = FastAPI()


# Lendo variáveis de ambiente
@lru_cache()
def get_settings():
    return Settings()


baseDadosTest = []  # Apenas para teste.

# Rota Raiz
@app.get("/",tags=["root"])
def root() -> dict:
    """Rota raiz"""
    return {"message": "Hello World"}  # Retornando um dicionário


@app.get("/users",tags=["users"],summary= 'Retorna as informações de cada usuario.')
def listando_date_user() -> list:
    """Listando todos dados"""
    return web.create_user(1000)


@app.get("/authUser", summary='Tenta autenticar o usuário')
def auth_user(username: str, password: str, response: Response, settings: Settings = Depends(get_settings)) -> bool:
    is_valid = auth.validate_user_credentials(username, password, settings)
    if not is_valid:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    return is_valid


@app.get("/authUserInfo", summary='Tenta autenticar usuário e retorna user info', status_code=status.HTTP_200_OK)
def auth_user_get_user_info(username: str, password: str, response: Response,
                            settings: Settings = Depends(get_settings)):
    user = auth.validate_credentials_get_user_info(username, password, settings)
    if user is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    return user


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

## Substituir
@app.get("/sensorsInfo",tags=["legacy"])
def get_sensors_info():
    return web.create_fake_sensors(10)
###################################################################################
#GET
@app.get("/sensors/{sensor_id}",tags=["sensors"],summary= 'Retorna as informações de um sensor específico.')
def get_sensor(sensor_id:int):
    return web.sensor_builder(sensor_id)

#GET
@app.get("/sensors",tags=["sensors"],summary= 'Retorna n sensores')
def get_sensors(n_sensors:int):
    return [web.sensor_builder(i) for i in range(1, n_sensors+1)]

@app.get("/history",tags=["history"],summary= 'Retorna o historico dos n dias de um sensor.')
def get_values(sensor_id:int, n_days:int):
    return web.build_temp_history(sensor_id, n_days)

#POST
@app.post("/sensors",tags=["sensors"],summary= 'Cria um sensor')
def create_sensor(my_sensor:web.MySensor):

    baseDadosTest.append(my_sensor) # Apenas para teste.

    web.add_sensor_to_db(my_sensor)

# #PATCH
@app.patch("/sensors/{id}",tags=["sensors"],summary= 'Cria um sensor')
def sensor(id:int, input_json:web.MySensor):
    web.patch_sensor(id, input_json)
