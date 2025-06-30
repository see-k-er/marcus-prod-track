from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models import User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    

    if current_user.role != 'admin':
        flash("Unauthorized access.")
        return redirect(url_for('worker.dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        is_active = request.form.get('is_active') == 'on'
        
        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("Username already exists.", "error")
        else:
            
            user = User(
                username=username,
                password_hash=generate_password_hash(password),
                role=role,
                is_active=is_active
            )
            db.session.add(user)
            db.session.commit()
            flash(f"User '{username}' created successfully!")
            return redirect(url_for('admin.create_user'))

    return render_template('admin/create_user.html')
