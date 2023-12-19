from dotenv import load_dotenv
# from pydantic import validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # SECRET_KEY: str
    KAFKA_URL: str
    MYSQL_URL: str
    # BACKEND_CORS_ORIGINS: str
    # JWT_SECRET_KEY: str
    # JWT_ALGORITHM: str = 'HS256'
    # JWT_EXPIRATION_DELTA: int
    CELERY_BROKER_URL: str
    REDIS_URL: str
    SERVER_PORT: int
    # @validator("BACKEND_CORS_ORIGINS")
    # def assemble_cors_origins(cls, v: str):
    #     return [i.strip() for i in v.split(",")]

    class Config:
        env_file = '.env'


settings = Settings()
