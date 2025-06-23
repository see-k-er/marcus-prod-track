# app/routes/management.py

from flask import Blueprint, render_template
from flask_login import login_required

management_bp = Blueprint('management', __name__)

@management_bp.route('/management/dashboard')
@login_required
def dashboard():
    return "<h2>management Dashboard (stub)</h2>"
