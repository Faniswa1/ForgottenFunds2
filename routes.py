import logging
import os
import stripe
import requests
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, UnclaimedFund
from datetime import datetime, timedelta
import random

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def create_routes(app):
    @app.route('/')
    @login_required
    def home():
        funds = UnclaimedFund.query.order_by(UnclaimedFund.date_found.desc()).all()
        return render_template('dashboard.html', funds=funds)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                flash("Username already exists")
                return render_template('register.html')
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user:
                login_user(user)
                flash(f"Welcome back, {user.username}!")
                return redirect(url_for('home'))
            flash("Invalid username or password")
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        logout_user()
        flash("You have been logged out")
        return redirect(url_for('home'))

    @app.route('/search', methods=['POST'])
    @login_required
    def search():
        name = request.form['name']
        results = search_unclaimed_funds(name)
        return render_template('search_results.html', results=results.get('results', []))

def search_unclaimed_funds(name):
    logging.debug(f"Searching for unclaimed funds for {name}")
    return {"results": [{"name": name, "amount": round(random.uniform(50, 1000), 2), "source": "Test Database"}]}
