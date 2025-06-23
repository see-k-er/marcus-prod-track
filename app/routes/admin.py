# app/routes/admin.py

from flask import Blueprint, render_template
from flask_login import login_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    return "<h2>Admin Dashboard (stub)</h2>"
