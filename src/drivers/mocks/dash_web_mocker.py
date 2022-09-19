# disable pylint(no-name-in-module)
import random
from pydantic import BaseModel

# Criando um modelo
class User(BaseModel):
    """   Rota raiz    """

    id: int
    email: str
    name: str
    password: str
    access: str

def create_user(num_user:int)-> list:
    num_user = (num_user *3)
    list_date_user = []
    for num in range(1,999,3):
        if(num%2):
            list_date_user.append(User(
                id=num,
                email=f"teste0{num}@gmail.com",
                name=f"nameteste{num}",
                password=f"123456{num}",
                access="Admin"))
        else:
            list_date_user.append(User(
                id=num,
                email=f"teste0{num}@gmail.com",
                name=f"nameteste{num}",
                password=f"123456{num}",
                access="User"))
    return list_date_user

def get_temp_history(init_temp:int,fim_temp:int,num_teste=20) -> list:
    """Retornando tempo para cada tipo de temperatura"""
    my_history = []
    for i in range(1, num_teste):
        my_history.extend(
            [
                {
                    "time": f"2022-09-{i}T{j}:00:00",
                    "temperature": random.uniform(init_temp,fim_temp),
                }
                for j in range(1, 24)
            ]
        )
    return my_history

def get_limite(init_temp=20,fim_temp=40):
    """Retornando tempo limite"""
    temp_atual = random.randint(init_temp,fim_temp)
    return {"litmit": temp_atual}

