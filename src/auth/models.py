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
    token: str

class UserGroup(BaseModel):
    user_id: str
    groups_ids: list[str]

class CreateUserData(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    password: str