import os
from urllib.parse import urlparse

# Get database URL from environment
db_url = os.environ.get("DATABASE_URL")

# Convert Render's PostgreSQL URL to SQLAlchemy 2.0 format
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
