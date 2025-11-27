from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    api_name: str = "Proxy API for Online Service"
    debug: bool = True

    base_url: str
    users_path: str
    protected_path: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
