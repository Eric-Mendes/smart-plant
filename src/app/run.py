import random
from fastapi import FastAPI
from pydantic import BaseModel
import src.drivers.mocks.dash_web_mocker as web


# Criando aplicação
app = FastAPI()


# Rota Raiz
@app.get("/")
def root() -> dict:
    """Rota raiz"""
    return {"message": "Hello World"}  # Retornando um dicionário

@app.get("/users")
def listando_date_user() -> BaseModel:
    """Listando todos dados"""
    return web.create_user(1000)

@app.get("/times")
def get_temp_history() -> list:
    """Retornando tempo para cada tipo de temperatura"""
    return web.get_temp_history(27,30,num_teste=10)
    
@app.get("/timeLimites")
def get_limite():
    """Retornando tempo limite"""
    return web.get_limite(20,40)


