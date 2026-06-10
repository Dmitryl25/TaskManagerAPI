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

    @computed_field
    @property
    def url(self) -> str:
        return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/0"


class TestDatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      extra='ignore')
    test_postgres_db: str
    test_postgres_user: str
    test_db_password: str
    test_postgres_host: str
    test_postgres_port: str

    @computed_field
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.test_postgres_user}:{self.test_db_password}@{self.test_postgres_host}:{self.test_postgres_port}/{self.test_postgres_db}"

class S3Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      extra='ignore')
    s3_access_key: str
    s3_secret_key: str
    s3_endpoint: str
    s3_bucket: str


class Settings(BaseSettings):
    jwt: JWTSettings = Field(default_factory=JWTSettings)
    database: DataBaseSettings = Field(default_factory=DataBaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    test_db: TestDatabaseSettings = Field(default_factory=TestDatabaseSettings)
    s3: S3Settings = Field(default_factory=S3Settings)

settings = Settings()