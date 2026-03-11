# Standard Library Imports
import time

# Third-Party Imports
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    app_name: str = "Retail Inventory API"
    version: str = "0.0.0"
    debug: bool = False
    db_username: str = ""
    db_password: str = ""
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "postgres"
    start_time: float = time.time()

    class Config:
        env_file = ".env"


config = Config()
