from pydantic import BaseSettings


class Settings(BaseSettings):
    kc_server_url: str
    kc_admin_usernanme: str = "admin"
    kc_admin_password: str = "admin"
    kc_realm_name: str = "master"
    kc_client_id: str = "admin-cli"

    class Config:
        env_file = ".env"
