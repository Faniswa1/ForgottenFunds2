import os

class Config:
    SECRET_KEY = os.getenv("SESSION_SECRET", "dev_secret_key_123")

    # Fix DATABASE_URL handling
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///site.db")  # Default for local dev
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)  # Render fix

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
