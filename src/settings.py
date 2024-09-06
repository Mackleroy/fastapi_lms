from functools import lru_cache, cached_property
from typing import Optional

from pydantic_settings import BaseSettings


class LMSBaseSettings(BaseSettings):
    """Base class for inheritance in purpose to dry main configurations"""

    class Config:
        env_file = "../.env"
        case_sensitive = False
        extra = "allow"


class DatabaseSettings(LMSBaseSettings):
    driver: str = "postgresql+asyncpg"
    host: str
    port: str
    user: str
    name: str
    password: Optional[str]

    @cached_property
    def test_database_name(self):
        return f"test_{self.name}"

    @cached_property
    def database_url(self):
        return (
            f"{self.driver}://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.name}"
        )

    class Config:
        env_prefix = "db_"


class Settings(LMSBaseSettings):
    database: DatabaseSettings = DatabaseSettings()


# Create an instance of the Settings class
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
