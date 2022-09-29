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


class Metrics(BaseModel):
    id: int
    metric_name: str
    metric: int


class Sensor(BaseModel):
    id: int
    sensor_name: str
    metrics: list
    has_exceeded_limit: bool


def create_fake_metrics(num_metrics: int) -> list:
    metrics_list = []

    for metric_id in range(1, num_metrics):
        metrics_list.append(
            Metrics(
                id=metric_id,
                metric_name="Temperatura {}".format(metric_id),
                metric=get_temp_atual(0, 100)
            )
        )
    return metrics_list


def create_fake_sensors(num_sensors: int) -> list:
    sensors_list = []

    for sensor_id in range(1, num_sensors):
        metrics = []
        for metric in range(1, 5):
            metrics.append(get_limit(20, 100))
        sensors_list.append(
            Sensor(
                id=sensor_id,
                sensor_name="Sensor{}".format(sensor_id),
                metrics=create_fake_metrics(3),
                has_exceeded_limit=get_has_exceeded_limit(sensor_id)
            )
        )
    return sensors_list


def create_user(num_user: int) -> list:
    num_user = (num_user * 3)
    list_date_user = []
    for num in range(1, 999, 3):
        if (num % 2):
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


def get_history(init_temp: int, fim_temp: int, n_days=20) -> list:
    """Retornando tempo para cada tipo de temperatura"""
    my_history = []
    for i in range(1, n_days):
        my_history.extend(
            [
                {
                    "time": f"2022-09-{i}T{j}:00:00",
                    "temperature": random.uniform(init_temp, fim_temp),
                }
                for j in range(1, 24)
            ]
        )
    return my_history


def get_limit(init_temp=20, fim_temp=40) -> dict:
    """Retornando tempo limite"""
    temp_atual = random.randint(init_temp, fim_temp)
    return {"limit": temp_atual}

def get_temp_atual(init_temp=20, fim_temp=40) -> int:
    return random.randint(init_temp, fim_temp)


def get_has_exceeded_limit(num: int) -> bool :
    return True if num % 2 else False
