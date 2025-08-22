import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    STRIPE_SECRET_KEY: str | None = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PRICE_ID: str | None = os.getenv("STRIPE_PRICE_ID")
    STRIPE_WEBHOOK_SECRET: str | None = os.getenv("STRIPE_WEBHOOK_SECRET")
    STRIPE_SUCCESS_URL: str | None = os.getenv("STRIPE_SUCCESS_URL")
    STRIPE_CANCEL_URL: str | None = os.getenv("STRIPE_CANCEL_URL")

settings = Settings()
