from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field, computed_field
import os

# Загрузка полей из .env

# для JWT
class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      extra='ignore')
    secret_key: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    algorithms: str

# для БД
class DataBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      extra='ignore')
    postgres_db: str
    postgres_user: str
    db_password: str
    postgres_host: str
    postgres_port: str

    @computed_field
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.db_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

# для redis
class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      extra='ignore')
    redis_password: str
    redis_host: str
    redis_port: str

class Settings(BaseSettings):
    jwt: JWTSettings = Field(default_factory=JWTSettings)
    database: DataBaseSettings = Field(default_factory=DataBaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)

settings = Settings()