"""App configuration — YOUR CODE, Task 1.3.

Contract (other modules rely on this):
    from config import settings
    settings.google_client_id      (str)
    settings.google_client_secret  (str)
    settings.session_secret        (str)
    settings.database_url          (str)
    settings.test_database_url     (str)
    settings.redirect_uri          (str)

Approach: a pydantic-settings `BaseSettings` subclass that reads backend/.env.
Why not os.environ reads scattered around the code? One validated object,
loud failure at startup if a variable is missing, one place to see every knob.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    google_client_id: str
    google_client_secret: str
    session_secret: str
    database_url: str
    test_database_url: str    
    redirect_uri: str
    
settings = Settings()
