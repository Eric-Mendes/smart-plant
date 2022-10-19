from fastapi import FastAPI, status, Response, Request

import src.auth.keycloak as auth
import src.drivers.mocks.dash_mocker as web
from fastapi.middleware.cors import CORSMiddleware

# Criando aplicação
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota Raiz
@app.get("/",tags=["root"])
def root() -> dict:
    """Rota raiz"""
    return {"message": "Hello World"}  # Retornando um dicionário


###### Validação Do Token #####
def validate_request(request, response, group):
    token = request.headers.get('Authorization')
    my_authorization = auth.verify_token_and_group(token, group)

    if(my_authorization["is_valid"] != True):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "msg": "invalid token"
        }

    elif(my_authorization["in_group"] != True):
        response.status_code = status.HTTP_403_FORBIDDEN

        return {
            "msg": "the owener of the token is not an administrator"
        }
    
    return True

###### Auth ######
@app.get("/authUser", tags=["auth"], summary='Tenta autenticar o usuário, retorna um token')
def auth_user(username: str, password: str, response: Response) -> bool:
    token = auth.validate_user_credentials(username, password)
    if token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "msg": "wrong username/password"
        }

    else:
        response.status_code = status.HTTP_202_ACCEPTED
        return {
            "access_token": token
        }


@app.get("/authUserInfo", tags=["auth"], summary='Tenta autenticar usuário e retorna user info', status_code=status.HTTP_200_OK)
def auth_user_get_user_info(username: str, password: str, response: Response):
    user = auth.validate_credentials_get_user_info(username, password)
    if user is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    return user

###### Validate #######
@app.get("/validate", tags=["validate"], summary='Verifica se um token é valido, se for, retorna informações do usuario')
def verify_token(request: Request):
    token = request.headers.get('Authorization')
    data = auth.getInfoByToken(token)

    if(data is None):
        return {
            "is_valid": False
        }

    else:
        return {
            "is_valid": True,
            **data,
            "groups": auth.get_user_kc_groups(data["sub"])
        }

######## User #########
@app.get("/user/list", tags=["user"], summary='Retorna uma lista de usuarios', status_code=status.HTTP_200_OK)
def get_users(request: Request, response: Response):
    validy = validate_request(request, response, "Admin")

    if(validy != True):
        return validy
        
    else:
        response.status_code = status.HTTP_200_OK

        return {
            "users" : auth.get_users()
        }

@app.post("/user", tags=["user"], summary= 'Cria um novo usuario, precisa do token de um admin')
def create_user(data: auth.CreateUserData, request: Request, response: Response):
    validy = validate_request(request, response, "Admin")

    if(validy != True):
        return validy

    created = auth.createUser(data)

    if(created == True):
        response.status_code = status.HTTP_201_CREATED
    else:
        response.status_code = status.HTTP_409_CONFLICT

@app.delete("/user", tags=["user"], summary= 'Deleta um usuario, precisa do token de um admin')
def delete_user(user_id: str, request: Request, response: Response):
    validy = validate_request(request, response, "Admin")

    if(validy != True):
        return validy

    deleted = auth.deleteUser(user_id)

    if(deleted == True):
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST

####### userGroups #######

@app.get("/userGroups", tags=["userGroups"], summary= 'Retorna os grupos de um dado id de usuario', status_code=status.HTTP_200_OK)
def get_user_groups(user_id, request: Request, response: Response):
    validy = validate_request(request, response, "Admin")

    if(validy != True):
        return validy

    else:
        groups = auth.get_user_kc_groups(user_id)

        return {
            "groups" : groups
        }

@app.post("/userGroups", tags=["userGroups"], summary='Adiciona um usuario a um grupo, precisa do token de um admin')
def add_to_group(item: auth.UserGroup, request: Request, response: Response) -> bool:
    validy = validate_request(request, response, "Admin")

    if(validy != True):
        return validy

    user_id = item.user_id
    group_list_ids = item.groups_ids

    for group_id in group_list_ids:
        auth.add_user_group(user_id, group_id)

@app.delete("/userGroups", tags=["userGroups"], summary='Remove um usuario de um grupo, precisa do token de um admin')
def remove(item: auth.UserGroup, request: Request, response: Response) -> bool:
    validy = validate_request(request, response, "Admin")

    if(validy != True):
        return validy

    user_id = item.user_id
    group_list_ids = item.groups_ids

    for group_id in group_list_ids:
        auth.remove_user_group(user_id, group_id)

####### groups ###########
@app.get("/groups/list", tags=["groups"], summary= 'Retorna os grupos de um dado id de usuario', status_code=status.HTTP_200_OK)
def get_groups(request: Request, response: Response):
    validy = validate_request(request, response, "Admin")

    if(validy != True):
        return validy

    else:
        groups = auth.get_groups()

        return {
            "groups" : groups
        }
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

    web.add_sensor_to_db(my_sensor)

# #PATCH
@app.patch("/sensors/{id}",tags=["sensors"],summary= 'Cria um sensor')
def sensor(id:int, input_json:web.MySensor):
    web.patch_sensor(id, input_json)
