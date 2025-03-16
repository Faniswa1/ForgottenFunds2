import os

uri = os.getenv("DATABASE_URL", "sqlite:///default.db")  # Get the env variable
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)  # Fix for SQLAlchemy

SQLALCHEMY_DATABASE_URI = uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

