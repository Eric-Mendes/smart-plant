import keycloak as kc
from pydantic import BaseModel
from typing import List, Optional

from src.drivers.interfaces.config import Settings


class KeycloakGroup(BaseModel):
    id: str
    name: str
    path: str


class KeycloakUser(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    created_timestamp: int
    groups: List[KeycloakGroup]


def validate_user_credentials(username: str, password: str, settings: Settings) -> bool:
    try:
        keycloak_openid = kc.KeycloakOpenID(
            server_url=settings.kc_server_url,
            realm_name=settings.kc_realm_name,
            client_id=settings.kc_client_id
        )
        keycloak_openid.token(username, password)
        return True
    except Exception as e:
        print(e)
        return False


def get_user_info(username: str, settings: Settings) -> KeycloakUser:
    try:
        keycloak_admin = kc.KeycloakAdmin(server_url=settings.kc_server_url,
                                          username=settings.kc_admin_usernanme,
                                          password=settings.kc_admin_password,
                                          realm_name=settings.kc_realm_name)
        user_id = keycloak_admin.get_user_id(username)
        user = keycloak_admin.get_user(user_id)
        groups = get_user_kc_groups(keycloak_admin, user_id)
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
        print(e)
        raise e


def get_user_kc_groups(keycloak_admin, user_id) -> List[KeycloakGroup]:
    user_groups = keycloak_admin.get_user_groups(user_id)
    kc_groups: List[KeycloakGroup] = []
    for group in user_groups:
        kc_group: KeycloakGroup = KeycloakGroup(
            id=group['id'],
            name=group['name'],
            path=group['path']
        )
        kc_groups.append(kc_group)

    return kc_groups


def validate_credentials_get_user_info(username: str, password: str, settings: Settings) -> Optional[KeycloakUser]:
    if validate_user_credentials(username, password, settings):
        return get_user_info(username, settings)
    else:
        return None
