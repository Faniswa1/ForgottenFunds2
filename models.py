from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class UnclaimedFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    possible_owner = db.Column(db.String(200), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(500), nullable=False)
    date_found = db.Column(db.DateTime, default=datetime.utcnow)
    last_known_address = db.Column(db.String(500), nullable=True)
    contact_info = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(100), default="Pending")
    notes = db.Column(db.Text, nullable=True)
