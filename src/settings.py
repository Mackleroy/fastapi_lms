from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create an instance of the Settings class
settings = Settings()
