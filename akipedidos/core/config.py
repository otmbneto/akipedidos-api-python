from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_name: str = "Proxy API for Online Service"
    debug: bool = True

    base_url: str
    login_path: str
    users_path: str
    protected_path: str
    panel_item_page: str
    panel_category_page: str
    action_get_register_category: str
    action_get_items_from_category: str
    action_edit_category: str
    action_remove_category: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
