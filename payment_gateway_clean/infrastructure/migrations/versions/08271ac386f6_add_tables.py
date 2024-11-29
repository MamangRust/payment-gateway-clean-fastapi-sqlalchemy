"""add tables

Revision ID: 08271ac386f6
Revises: 
Create Date: 2024-11-29 01:54:38.949577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '08271ac386f6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'users' table
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('firstname', sa.String(100), nullable=False),
        sa.Column('lastname', sa.String(100), nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('password', sa.String(100), nullable=False),
        sa.Column('noc_transfer', sa.String(255), unique=True, nullable=False, default="0"),
        sa.Column('created_at', sa.TIMESTAMP, server_default=func.current_timestamp()),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    )

    # Create the 'topups' table
    op.create_table(
        'topups',
        sa.Column('topup_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('topup_no', sa.Text, nullable=False),
        sa.Column('topup_amount', sa.Integer, nullable=False),
        sa.Column('topup_method', sa.Text, nullable=False),
        sa.Column('topup_time', sa.TIMESTAMP, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=func.current_timestamp()),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    )

    # Create the 'saldo' table
    op.create_table(
        'saldo',
        sa.Column('saldo_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('total_balance', sa.Integer, nullable=False),
        sa.Column('withdraw_amount', sa.Integer, default=0),
        sa.Column('withdraw_time', sa.TIMESTAMP),
        sa.Column('created_at', sa.TIMESTAMP, server_default=func.current_timestamp()),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    )

    # Create the 'transfers' table
    op.create_table(
        'transfers',
        sa.Column('transfer_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('transfer_from', sa.Integer, sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('transfer_to', sa.Integer, sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('transfer_amount', sa.Integer, nullable=False, default=0),
        sa.Column('transfer_time', sa.TIMESTAMP, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=func.current_timestamp()),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    )

    # Create the 'withdraws' table
    op.create_table(
        'withdraws',
        sa.Column('withdraw_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('withdraw_amount', sa.Integer, nullable=False),
        sa.Column('withdraw_time', sa.TIMESTAMP, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=func.current_timestamp()),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    )

def downgrade():
    # Drop the tables in reverse order to maintain referential integrity
    op.drop_table('withdraws')
    op.drop_table('transfers')
    op.drop_table('saldo')
    op.drop_table('topups')
    op.drop_table('users')
