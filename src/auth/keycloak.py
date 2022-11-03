import keycloak as kc
from typing import List, Optional
from .config import get_settings
from .models import *

from src.auth.config import Settings

def getKeyCloakOpenId():
    settings = get_settings()

    return kc.KeycloakOpenID(
        server_url=settings.kc_server_url,
        realm_name=settings.kc_realm_name,
        client_id=settings.kc_client_id
    )

def getKeyCloakAdmin():
    settings = get_settings()

    return kc.KeycloakAdmin(
        server_url=settings.kc_server_url,
        username=settings.kc_admin_usernanme,
        password=settings.kc_admin_password,
        realm_name=settings.kc_realm_name
    )

# Funções relacionados a autenticação e dados do usuario
def validate_user_credentials(username: str, password: str):
    try:
        keycloak_open_id = getKeyCloakOpenId()
        token = keycloak_open_id.token(username, password)

        return token["access_token"]

    except Exception as e:

        return None

def getInfoByToken(token: str):
    try:
        if("Bearer" in token):
            token = token.split()[-1]

        keycloak_open_id = getKeyCloakOpenId()
        data = keycloak_open_id.userinfo(token)
    
        return data

    except Exception as e:

        return None


def get_user_info(username: str) -> KeycloakUser:
    try:
        keycloak_admin = getKeyCloakAdmin()

        user_id = keycloak_admin.get_user_id(username)
        user = keycloak_admin.get_user(user_id)

        groups = get_user_kc_groups(user_id)
        kc_user: KeycloakUser = KeycloakUser(
            id=user['id'],
            username=user['username'],
            first_name=user['firstName'],
            last_name=user['lastName'],
            created_timestamp=user['createdTimestamp'],
            groups=groups
        )

        return kc_user

    except Exception as e:
        raise e

def validate_credentials_get_user_info(username: str, password: str, settings: Settings) -> Optional[KeycloakUser]:
    if validate_user_credentials(username, password, settings):
        return get_user_info(username, settings)
    else:
        return None

## Funções Relacionadas a grupos
def get_groups():
    keycloak_admin = getKeyCloakAdmin()
    groups = keycloak_admin.get_groups()
    
    return groups

def get_user_kc_groups(user_id) -> List[KeycloakGroup]:
    keycloak_admin = getKeyCloakAdmin()
    user_groups = keycloak_admin.get_user_groups(user_id)

    kc_groups: List[KeycloakGroup] = []
    for group in user_groups:
        kc_group: KeycloakGroup = KeycloakGroup(
            id= group['id'],
            name= group['name'],
            path= group['path']
        )
        kc_groups.append(kc_group)

    return kc_groups

def add_user_group(user_id, user_group):
    try:
        keycloak_admin = getKeyCloakAdmin()
        keycloak_admin.group_user_add(user_id, user_group)
        return True
    except:
        return False

def remove_user_group(user_id, user_group):
    try:
        keycloak_admin = getKeyCloakAdmin()
        keycloak_admin.group_user_remove(user_id, user_group)
        return True
    except:
        return False

def create_new_group(group_name):
    try:
        keycloak_admin = getKeyCloakAdmin()
        keycloak_admin.create_group({
            "name": group_name
        })
        return True
    except:
        return False

def delete_group(group_id):
    try:
        keycloak_admin = getKeyCloakAdmin()
        keycloak_admin.delete_group(group_id)
        return True
    except:
        return False

## Funções Relacionadas a usuarios
def get_users():
    keycloak_admin = getKeyCloakAdmin()
    user_groups = keycloak_admin.get_users()

    return user_groups

def createUser(data: CreateUserData):
    try:
        keycloak_admin = getKeyCloakAdmin()
        keycloak_admin.create_user(        
            payload={
                    "username": data.username,
                    "email": data.email,
                    "firstName": data.firstName,
                    "lastName": data.lastName,
                    "enabled": True,
                    "credentials":[{
                        "value": data.password
                    }]
                })

        return True
    
    except Exception as e:
        return False

def deleteUser(user_id):
    try:
        keycloak_admin = getKeyCloakAdmin()
        keycloak_admin.delete_user(user_id)

        return True
    
    except Exception as e:
        return False


# Diversos
def verify_token_and_group(token, desired_group):
    is_valid = False
    in_group = False

    if(token != None):
        if("Bearer" in token):
            token = token.split()[-1]
        
        data = getInfoByToken(token)
        if(data != None):
            is_valid = True
            my_groups = get_user_kc_groups(data["sub"])

            groups = [group.name for group in my_groups]

            if(isinstance(desired_group, str) and desired_group in groups):
                in_group = True
            
            elif(isinstance(desired_group, list)):
                in_group = any(x in desired_group for x in groups)

    return {
        "is_valid": is_valid,
        "in_group": in_group
    }