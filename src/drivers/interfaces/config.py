from pydantic import BaseSettings


class Settings(BaseSettings):
    kc_server_url: str
    kc_admin_usernanme: str
    kc_admin_password: str
    kc_realm_name: str
    kc_client_id: str

    class Config:
        env_file = ".env"
