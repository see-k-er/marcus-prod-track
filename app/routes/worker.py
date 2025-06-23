# app/routes/worker.py

from flask import Blueprint, render_template
from flask_login import login_required

worker_bp = Blueprint('worker', __name__)

@worker_bp.route('/worker/dashboard')
@login_required
def dashboard():
    return "<h2>Worker Dashboard (stub)</h2>"
