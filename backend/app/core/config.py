from pydantic_settings import BaseSettings


class Settings(BaseSettings):
APP_NAME: str = "TradeBot API"
API_V1_PREFIX: str = "/api/v1"


# DB & Security
DATABASE_URL: str = "postgresql+psycopg://tradebot:tradebot@db:5432/tradebot"
JWT_SECRET: str = "change-me"
JWT_EXPIRE_MIN: int = 60 * 24


# Crypto for AES-256-GCM
MASTER_KEY: str = "change-this-master-key" # используется для деривации AES-ключей


# TradingView webhook
TV_WEBHOOK_SECRET: str = "change-webhook-secret"


# CORS
CORS_ORIGINS: list[str] = ["*"]


class Config:
env_file = ".env"


settings = Settings()