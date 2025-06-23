# app/models.py

from datetime import datetime
from flask_login import UserMixin
from . import db

### 1. Department ###
class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    users = db.relationship('User', backref='department', lazy=True)
    machines = db.relationship('Machine', backref='department', lazy=True)

### 2. User ###
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, management, worker
    is_active = db.Column(db.Boolean, default=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    shifts = db.relationship('Shift', backref='user', lazy=True)
    plans = db.relationship('MachinePlan', backref='user', lazy=True)

### 3. Machine ###
class Machine(db.Model):
    __tablename__ = 'machines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    type = db.Column(db.String(64), nullable=True)  # e.g., "90T"
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    plans = db.relationship('MachinePlan', backref='machine', lazy=True)
    part_mappings = db.relationship('PartMachine', backref='machine', lazy=True)

### 4. Part ###
class Part(db.Model):
    __tablename__ = 'parts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(64), unique=True, nullable=False)
    customer = db.Column(db.String(128))
    material = db.Column(db.String(128))
    weight = db.Column(db.Float)
    price = db.Column(db.Float)

    # Per-hour outputs
    pdc_machine = db.Column(db.String(64))
    pdc_output = db.Column(db.Integer)
    fettling_output = db.Column(db.Integer)
    machining_op1_output = db.Column(db.Integer)
    machining_op2_output = db.Column(db.Integer)
    machining_op3_output = db.Column(db.Integer)
    machining_op4_output = db.Column(db.Integer)
    vibro_output = db.Column(db.Integer)
    shot_blasting_output = db.Column(db.Integer)
    powder_coating_output = db.Column(db.Integer)
    plating_output = db.Column(db.Integer)
    assembly_rubber_pad_output = db.Column(db.Integer)
    assembly_plug_output = db.Column(db.Integer)
    final_inspection_output = db.Column(db.Integer)
    packing_output = db.Column(db.Integer)
    production_sequence = db.Column(db.String(256))

    part_mappings = db.relationship('PartMachine', backref='part', lazy=True)
    logs = db.relationship('ProductionLog', backref='part', lazy=True)

### 5. PartMachine ###
class PartMachine(db.Model):
    __tablename__ = 'part_machine'

    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id'), nullable=False)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False)

### 6. Shift ###
class Shift(db.Model):
    __tablename__ = 'shifts'
    __table_args__ = (db.UniqueConstraint('name', 'date', 'user_id'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)  # Day/Night
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    plans = db.relationship('MachinePlan', backref='shift', lazy=True)

### 7. MachinePlan ###
class MachinePlan(db.Model):
    __tablename__ = 'machine_plans'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'), nullable=False)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False)
    status = db.Column(db.String(32), nullable=False)  # Planned / Breakdown / No Plan
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    logs = db.relationship('ProductionLog', backref='machine_plan', lazy=True)

### 8. ProductionLog ###
class ProductionLog(db.Model):
    __tablename__ = 'production_logs'
    __table_args__ = (db.UniqueConstraint('machine_plan_id', 'hour_slot'),)

    id = db.Column(db.Integer, primary_key=True)
    machine_plan_id = db.Column(db.Integer, db.ForeignKey('machine_plans.id'), nullable=False)
    hour_slot = db.Column(db.Integer, nullable=False)  # 1 to 12 for 9AM to 9PM
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id'), nullable=False)
    remarks = db.Column(db.String(64), nullable=False, default="Running")
    qty_ok = db.Column(db.Integer, default=0)
    qty_rej = db.Column(db.Integer, default=0)
    qty_rew = db.Column(db.Integer, default=0)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

### 9. Variable ###
class Variable(db.Model):
    __tablename__ = 'variables'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    value = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))

