# disable pylint(no-name-in-module)

# import requests
# import isodate
# from datetime import timedelta
from fastapi import FastAPI
from pydantic import BaseModel
import random

# from typing import Optional
# from mangum import Mangum


# Criando aplicação
app = FastAPI()


# Rota Raiz
@app.get("/")
def root() -> dict:
    """Rota raiz"""
    return {"message": "Hello World"}  # Retornando um dicionário


# Criando um modelo
class User(BaseModel):
    """Rota raiz"""

    id: int
    email: str
    name: str
    password: str
    access: str


date_user = [
    User(
        id=1,
        email="teste01@gmail.com",
        name="nameteste01",
        password="123456",
        access="Admin",
    ),
    User(
        id=2,
        email="teste02@gmail.com",
        name="nameteste02",
        password="729012",
        access="Admin",
    ),
    User(
        id=3,
        email="teste03@gmail.com",
        name="nameteste03",
        password="289012",
        access="User",
    ),
    User(
        id=4,
        email="teste04@gmail.com",
        name="nameteste04",
        password="289012",
        access="User",
    ),
]


@app.get("/users")
def listando_date_user() -> BaseModel:
    """Listando todos dados"""
    return date_user


@app.get("/times")
def get_temp_history() -> list:
    """Retornando tempo para cada tipo de temperatura"""
    my_history = []
    for i in range(1, 10):
        my_history.extend(
            [
                {
                    "time": f"2022-09-{i}T{j}:00:00",
                    "temperature": random.uniform(20, 27),
                }
                for j in range(1, 24)
            ]
        )

    return my_history


@app.get("/timeLimites")
def get_limite():
    """Retornando tempo limite"""
    limit = {"Limite": 25}
    return limit


# #Criando Base de dados

# baseDados = [
#     User(id=1, email='teste01@gmail.com',name='nameteste01',password='123456'),
#     User(id=2, email='teste02@gmail.com',name='nameteste02',password='789012')
# ]


# # get All
# @app.get('/users')
# def listandoUsuarios():
#     return baseDados


# # verificando usuarios
# @app.get('/users/{id}')
# def verificauser(idUser:int):
#     for user in baseDados:
#         if user.id == idUser:
#             return user
#     return {"message": "User not found"}

# #Inserindo usuarios
# @app.post('/users')
# def inserindoUsuarios(user:User):
#     baseDados.append(user)
#     return user #Retornando o usuario inserido

# @app.delete('/users/{id}')
# def deletandoUsuarios(idUser:int):
#     for user in baseDados:
#         if user.id == idUser:
#             baseDados.remove(user)
#             return {"message": "User deleted"}
#     return {"message": "User not found"}


# class User(BaseModel):
#     id:str

# @app.post('/tempos/{id}')
# def tempos(tempos:str):
#     #videos_id = getVideosID('PLqjGh_6v1ET9ASBdekaRTI73xwXUlajve')
#     videos_id = getVideosID(f'{id}')
#     print(videos_id)
#     videos_id = id
#     total = timedelta(seconds= 0)
#     for id in videos_id:
#         # print(id)
#         try:
#             duration = get_youtube_video_duration(id)
#         except:
#             continue
#         total += duration
#     print({"message": total})
#     return {"message": total}
