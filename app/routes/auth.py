# app/routes/auth.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app.models import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            print(f"Logging in user: {user.username if user else 'None'}")
            if user.role == 'admin':
                return redirect(url_for('admin.create_user'))
            elif user.role == 'management':
                return redirect(url_for('management.dashboard'))
            else:
                return redirect(url_for('worker.dashboard'))
        flash('Invalid username or password')
        

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
