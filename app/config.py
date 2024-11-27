from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    api_base_url: Optional[str] = "https://api.example.com"
    mapmyindia_client_id: Optional[str]
    mapmyindia_client_secret: Optional[str] 

    class Config:
        env_file = ".env"


settings = Settings()
