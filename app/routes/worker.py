from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Department, Machine, Shift, MachinePlan
from app.extensions import db
from datetime import datetime, date

# ✅ Define your blueprint BEFORE using it
worker_bp = Blueprint('worker', __name__, url_prefix='/worker')

@worker_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'worker':
        return redirect(url_for('auth.login'))

    departments = Department.query.order_by(Department.name).all()
    return render_template('worker/department_select.html', departments=departments)

@worker_bp.route('/department/<int:department_id>/plan', methods=['GET', 'POST'])
@login_required
def machine_planning(department_id):
    if current_user.role != 'worker':
        return redirect(url_for('auth.login'))

    machines = Machine.query.filter_by(department_id=department_id).all()
    shift_name = "Day" if 9 <= datetime.now().hour < 21 else "Night"
    today = date.today()

    shift = Shift.query.filter_by(user_id=current_user.id, name=shift_name, date=today).first()
    if not shift:
        shift = Shift(name=shift_name, date=today, user_id=current_user.id)
        db.session.add(shift)
        db.session.commit()

    if request.method == 'POST':
        for machine in machines:
            status = request.form.get(f"status_{machine.id}")
            if status:
                plan = MachinePlan.query.filter_by(shift_id=shift.id, machine_id=machine.id).first()
                if not plan:
                    plan = MachinePlan(
                        shift_id=shift.id,
                        machine_id=machine.id,
                        status=status,
                        user_id=current_user.id,
                        date=today
                    )
                    db.session.add(plan)
                else:
                    plan.status = status
        db.session.commit()
        return redirect(url_for('worker.machine_planning', department_id=department_id))

    plans = {
        plan.machine_id: plan.status
        for plan in MachinePlan.query.filter_by(shift_id=shift.id).all()
    }

    return render_template(
        'worker/machine_plan.html',
        machines=machines,
        shift_name=shift_name,
        plans=plans
    )
