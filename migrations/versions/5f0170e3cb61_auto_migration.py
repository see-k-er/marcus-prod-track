"""Auto migration

Revision ID: 5f0170e3cb61
Revises: 
Create Date: 2025-06-23 04:41:18.077939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f0170e3cb61'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('parts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('code', sa.String(length=64), nullable=False),
    sa.Column('customer', sa.String(length=128), nullable=True),
    sa.Column('material', sa.String(length=128), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('pdc_machine', sa.String(length=64), nullable=True),
    sa.Column('pdc_output', sa.Integer(), nullable=True),
    sa.Column('fettling_output', sa.Integer(), nullable=True),
    sa.Column('machining_op1_output', sa.Integer(), nullable=True),
    sa.Column('machining_op2_output', sa.Integer(), nullable=True),
    sa.Column('machining_op3_output', sa.Integer(), nullable=True),
    sa.Column('machining_op4_output', sa.Integer(), nullable=True),
    sa.Column('vibro_output', sa.Integer(), nullable=True),
    sa.Column('shot_blasting_output', sa.Integer(), nullable=True),
    sa.Column('powder_coating_output', sa.Integer(), nullable=True),
    sa.Column('plating_output', sa.Integer(), nullable=True),
    sa.Column('assembly_rubber_pad_output', sa.Integer(), nullable=True),
    sa.Column('assembly_plug_output', sa.Integer(), nullable=True),
    sa.Column('final_inspection_output', sa.Integer(), nullable=True),
    sa.Column('packing_output', sa.Integer(), nullable=True),
    sa.Column('production_sequence', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('variables',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('value', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('machines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('type', sa.String(length=64), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('part_machine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('part_id', sa.Integer(), nullable=False),
    sa.Column('machine_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['machine_id'], ['machines.id'], ),
    sa.ForeignKeyConstraint(['part_id'], ['parts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shifts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=16), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'date', 'user_id')
    )
    op.create_table('machine_plans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('shift_id', sa.Integer(), nullable=False),
    sa.Column('machine_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=32), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['machine_id'], ['machines.id'], ),
    sa.ForeignKeyConstraint(['shift_id'], ['shifts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('production_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('machine_plan_id', sa.Integer(), nullable=False),
    sa.Column('hour_slot', sa.Integer(), nullable=False),
    sa.Column('part_id', sa.Integer(), nullable=False),
    sa.Column('remarks', sa.String(length=64), nullable=False),
    sa.Column('qty_ok', sa.Integer(), nullable=True),
    sa.Column('qty_rej', sa.Integer(), nullable=True),
    sa.Column('qty_rew', sa.Integer(), nullable=True),
    sa.Column('submitted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['machine_plan_id'], ['machine_plans.id'], ),
    sa.ForeignKeyConstraint(['part_id'], ['parts.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('machine_plan_id', 'hour_slot')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('production_logs')
    op.drop_table('machine_plans')
    op.drop_table('shifts')
    op.drop_table('part_machine')
    op.drop_table('users')
    op.drop_table('machines')
    op.drop_table('variables')
    op.drop_table('parts')
    op.drop_table('departments')
    # ### end Alembic commands ###
