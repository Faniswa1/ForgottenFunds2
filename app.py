import os
import logging
import stripe
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, User, UnclaimedFund
from routes import create_routes
from config import Config
from werkzeug.security import generate_password_hash

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Ensure database URI is set
if not app.config.get("SQLALCHEMY_DATABASE_URI"):
    logging.error("SQLALCHEMY_DATABASE_URI is not set! Check your environment variables.")
else:
    logging.info(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Initialize database
db.init_app(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"  # Extra session security

@login_manager.user_loader
def load_user(user_id):
    try:
        user = User.query.get(int(user_id))
        if user is None:
            logging.warning(f"User with ID {user_id} not found.")
        return user
    except Exception as e:
        logging.error(f"Error loading user {user_id}: {e}")
        return None

# Register routes
create_routes(app)

# Ensure database tables exist and create admin user
with app.app_context():
    try:
        db.create_all()

        # Fetch admin credentials from environment variables
        ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'default_admin')
        ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'change_this')

        # Check if admin user exists
        if not User.query.filter_by(username=ADMIN_USERNAME).first():
            admin_user = User(
                username=ADMIN_USERNAME, 
                email=ADMIN_EMAIL, 
                password=generate_password_hash(ADMIN_PASSWORD),  # Hash password
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            logging.info("Admin user created successfully")
        else:
            logging.info("Admin user already exists.")
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
