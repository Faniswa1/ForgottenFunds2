import os
import logging
import stripe
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, User, UnclaimedFund
from routes import create_routes
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register routes
create_routes(app)

# Create tables and initialize admin user securely
with app.app_context():
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
            password=ADMIN_PASSWORD,  # Ensure you hash this before saving
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        logging.info("Admin user created successfully")

if __name__ == "__main__":
    app.run(debug=True)
