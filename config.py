import os

uri = os.getenv("DATABASE_URL", "sqlite:///site.db")  # Default to SQLite for local use
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)  # Fix for SQLAlchemy compatibility

SQLALCHEMY_DATABASE_URI =postgresql://root:rF5BQJQMVaeBx0MMMcg8xFdqF249ldRr@dpg-cvbkn7ofnakc73dm2edg-a/unclaimed_funds
SQLALCHEMY_TRACK_MODIFICATIONS = False
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET", "supersecretkey")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
MISSING_MONEY_API_KEY = os.getenv("MISSING_MONEY_API_KEY", "")


 


