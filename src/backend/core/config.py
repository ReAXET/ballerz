import os
from pydantic_core.core_schema import FieldValidationInfo
from pydantic import PostgresDsn, EmailStr, AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any
from enum import Enum
import secrets
from backend.paths import ROOT_DIR





class ModeEnum(str, Enum):
    DEV = "dev"
    PROD = "prod"
    TEST = "test"
    STAGING = "staging"



class Settings(BaseSettings):
    """
    Base settings class for the application configuration.  Utilizes pydantic_settings for
    configuration management.  This class is responsible for loading the configuration from
    the environment and validating the configuration values.
    """
    # Model Config for pydantic_settings
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=os.path.join(ROOT_DIR, ".env"),
        env_file_encoding="utf-8",

    )

    # Application Configuration
    APP_NAME: str = "ballerz"
    MODE: ModeEnum = ModeEnum.DEV
    API_VERSION: str = "v1"
    API_V1_STR: str = "/api/v1"
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 1 # 1 hour
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 100 # 100 days
    OPENAI_API_KEY: str = ""

    # Database Configuration
    TEMBO_DATABASE: str = os.getenv("POSTGRES_DATABASE", "")
    TEMBO_USERNAME: str = os.getenv("POSTGRES_USERNAME", "")
    TEMBO_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    TEMBO_HOST: str = os.getenv("POSTGRES_HOST", "")
    TEMBO_PORT: str = os.getenv("POSTGRES_PORT", "")
    TEMBO_DATABASE_URI: PostgresDsn | str = ""  # Postgres Database URI                                     

    # Trying out Prisma ORM. Disregard if not needed
    PRISMA_DB_URL: str = os.getenv("DATABASE_URL", "")

    
    # Neon Database Configuration
    NEON_DB_NAME: str = os.getenv("NEON_DB_NAME", "")
    NEON_USERNAME: str = os.getenv("NEON_USERNAME", "")
    NEON_CONNECT_ARGS: dict = {"sslmode": "require"}
    NEON_PASSWORD: str = os.getenv("NEON_PASSWORD", "")
    NEON_HOSTNAME: str = os.getenv("NEON_HOSTNAME", "")
    NEON_PORT: int = 5432
    NEON_DATABASE_URI: PostgresDsn | str = ""


    # Redis Configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Superuser Configuration
    FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER", "")
    FIRST_SUPERUSER_EMAIL: EmailStr = os.getenv("FIRST_SUPERUSER_EMAIL", "test@example.com")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "")

    # JWT Configuration
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENCRYPTION_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"




    





settings = Settings()