import keycloak as kc
from pydantic import BaseModel
from typing import List, Optional


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


def validate_user_credentials(username: str, password: str) -> bool:
    try:
        keycloak_openid = kc.KeycloakOpenID(
            server_url="http://172.19.0.1:8080/",
            realm_name="master",
            client_id="admin-cli"
        )
        keycloak_openid.token(username, password)
        return True
    except Exception as e:
        print(e)
        return False


def get_user_info(username: str) -> KeycloakUser:
    try:
        keycloak_admin = kc.KeycloakAdmin(server_url="http://172.19.0.1:8080/",
                                          username='admin',
                                          password='admin',
                                          realm_name="master")
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


def validate_credentials_get_user_info(username: str, password: str) -> Optional[KeycloakUser]:
    if validate_user_credentials(username, password):
        return get_user_info(username)
    else:
        return None
