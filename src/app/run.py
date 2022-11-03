from fastapi import FastAPI, status, Response, Request

import src.auth.keycloak as auth

from fastapi.middleware.cors import CORSMiddleware

import src.db.MongoConnection as mongo

# Criando aplicação
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO = mongo.MongoConnection()

# Rota Raiz
@app.get("/",tags=["root"])
def root() -> dict:
    """Rota raiz"""
    return {"message": "Hello World"}  # Retornando um dicionário


###### Validação Do Token #####
def validate_request(request, response, group:str | list):
    token = request.headers.get('Authorization')
    my_authorization = auth.verify_token_and_group(token, group)

    if(my_authorization["is_valid"] != True):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "msg": "invalid token"
        }

    elif(group != None and my_authorization["in_group"] != True):

        response.status_code = status.HTTP_403_FORBIDDEN

        return {
            "msg": "the owener of the token is not on authorized group"  
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

@app.post("/groups", tags=["groups"], summary= 'Cria um grupo novo', status_code=status.HTTP_201_CREATED)
def create_group(group_name:str, request: Request, response: Response):
    validy = validate_request(request, response, "Admin")

    if(validy != True):
        return validy

    else:
        created = auth.create_new_group(group_name)

        if(created == True):
            response.status_code = status.HTTP_201_CREATED
        else:
            response.status_code = status.HTTP_409_CONFLICT

@app.delete("/groups", tags=["groups"], summary= 'Deleta um grupo', status_code=status.HTTP_202_ACCEPTED)
def create_group(group_id:str, request: Request, response: Response):
    validy = validate_request(request, response, "Admin")

    if(validy != True):
        return validy

    else:
        created = auth.delete_group(group_id)

        if(created == True):
            response.status_code = status.HTTP_202_ACCEPTED
        else:
            response.status_code = status.HTTP_409_CONFLICT

#### Sensors #####
@app.get("/sensors/list", tags=["sensors"], summary= 'Retorna a lista de sensores referente aos grupos do usuario', status_code=status.HTTP_200_OK)
def getSensors(request: Request, response: Response):
    validate= validate_request(request, response, None)

    if(validate is True):
        my_data = MONGO.get_sensors_list()
        
        token = request.headers.get('Authorization')
        user_data = auth.getInfoByToken(token)

        user_groups = [group.name for group in auth.get_user_kc_groups(user_data["sub"])]

        filtered_sensors = [sensor for sensor in my_data if len(list(set(user_groups) & set(sensor["groups"]))) != 0]

        for sensor in filtered_sensors:
            for info in sensor["info"]:
                info["last_value"] = MONGO.get_last_telemetry(sensor["sensor_id"], info["type"])
        
        return filtered_sensors
    
    else:
        return validate

@app.get("/sensors", tags=["sensors"], summary= 'Retorna um sensor dado um id, precisa de um token valido para o sensor', status_code=status.HTTP_200_OK)
def getOneSensor(sensor_id, request: Request, response: Response):
    my_data = MONGO.get_sensor(sensor_id)
    
    if(len(my_data) != 0):
        groups = my_data[0]["groups"]
    else:
        groups = None

    validate = validate_request(request, response, groups)

    if(validate == True):
        if(len(my_data) != 0):
            return my_data[0]
    else:
        return validate

@app.patch("/sensors", tags=["sensors"], summary= 'Altera um sensor, usuario deve pertencer ao grupo', status_code=status.HTTP_200_OK)
def patchSensor(sensor_id, data: mongo.SensorPatch, request: Request, response: Response):
    my_data = MONGO.get_sensor(sensor_id)
    
    if(len(my_data) != 0):
        groups = my_data[0]["groups"]
    else:
        groups = None

    validate = validate_request(request, response, groups)
    
    if(validate == True):
        if(len(my_data) != 0):
            MONGO.patch_sensor(sensor_id, data)
    else:
        return validate

@app.post("/sensors/groups", tags=["sensors"], summary= 'Adiciona um grupo ao sensor', status_code=status.HTTP_200_OK)
def addGroupToSensor(sensor_id:str, group_name:str, request: Request, response: Response):
    validy = validate_request(request, response, "Admin")

    if(validy != True):
        return validy

    MONGO.addGroup(sensor_id, group_name)

@app.delete("/sensors/groups", tags=["sensors"], summary= 'Deleta um grupo de um sensor', status_code=status.HTTP_200_OK)
def removeGroupOfSensor(sensor_id:str, group_name:str, request: Request, response: Response):
    validy = validate_request(request, response, "Admin")

    if(validy != True):
        return validy

    MONGO.removeGroup(sensor_id, group_name)

##### Telemetry ######
@app.get("/telemetry/list", tags=["telemetry"], summary= 'Retorna a telemetria referente aos grupos do usuario', status_code=status.HTTP_200_OK)
def getTelemetryList(request: Request, response: Response):
    validate= validate_request(request, response, None)
    if(validate is True):
        telemetry_list = MONGO.get_telemetry_list()
        sensors_list = MONGO.get_sensors_list()
        
        sensor_groups = {}
        for data in sensors_list:
            sensor_groups[data["sensor_id"]] = data["groups"]

        token = request.headers.get('Authorization')
        user_data = auth.getInfoByToken(token)

        user_groups = [group.name for group in auth.get_user_kc_groups(user_data["sub"])]

        return [
            telemetry for telemetry in telemetry_list for my_group in user_groups if my_group in sensor_groups[telemetry["sensor_id"]]
            ]
    else:
        return validate
    
@app.get("/telemetry", tags=["telemetry"], summary= 'Retorna a telemetria dado um id de sensor, precisa de um token valido para o sensor', status_code=status.HTTP_200_OK)
def getSensorTelemetry(sensor_id, request: Request, response: Response):
    my_data = MONGO.get_sensor(sensor_id)
    
    if(len(my_data) != 0):
        groups = my_data[0]["groups"]
    else:
        groups = None

    validate = validate_request(request, response, groups)

    if(validate == True):
        if(len(my_data) != 0):
            telemetry = MONGO.get_sensor_telemetry(sensor_id)
            return telemetry
    else:
        return validate
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



############ mock #################
## Substituir
# @app.get("/sensorsInfo",tags=["legacy"])
# def get_sensors_info():
#     return web.create_fake_sensors(10)
# ###################################################################################
# #GET
# @app.get("/sensors/{sensor_id}",tags=["sensors"],summary= 'Retorna as informações de um sensor específico.')
# def get_sensor(sensor_id:int):
#     return web.sensor_builder(sensor_id)

# #GET
# @app.get("/sensors",tags=["sensors"],summary= 'Retorna n sensores')
# def get_sensors(n_sensors:int):
#     return [web.sensor_builder(i) for i in range(1, n_sensors+1)]

# @app.get("/history",tags=["history"],summary= 'Retorna o historico dos n dias de um sensor.')
# def get_values(sensor_id:int, n_days:int):
#     return web.build_temp_history(sensor_id, n_days)

# #POST
# @app.post("/sensors",tags=["sensors"],summary= 'Cria um sensor')
# def create_sensor(my_sensor:web.MySensor):

#     web.add_sensor_to_db(my_sensor)

# # #PATCH
# @app.patch("/sensors/{id}",tags=["sensors"],summary= 'Cria um sensor')
# def sensor(id:int, input_json:web.MySensor):
#     web.patch_sensor(id, input_json)