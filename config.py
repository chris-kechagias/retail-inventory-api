from pydantic_settings import BaseSettings


class Config(BaseSettings):
    app_name: str = "Retail Inventory API"
    version: str = "0.0.0"
    debug: bool = False
    db_username: str = ""
    db_password: str = ""

    class Config:
        env_file = ".env"

@property
def database_url(self) -> str:
    """
    Constructs the PostgreSQL connection string using the provided credentials.
    The format is:
    postgresql://username:password@host:port/database
    """
    return f"postgresql://{self.db_username}:{self.db_password}@localhost:5432/retail_inventory_db"

config = Config()