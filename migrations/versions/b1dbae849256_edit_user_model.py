"""edit_user_model

Revision ID: b1dbae849256
Revises: e6478e347700
Create Date: 2024-04-14 00:56:09.560818

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b1dbae849256'
down_revision = 'e6478e347700'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', mysql.VARCHAR(length=500), nullable=False))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
