"""add_new_table

Revision ID: e08764c7ec5e
Revises: 
Create Date: 2024-03-24 22:14:28.089501

"""
from alembic import op

# revision identifiers, used by Alembic.
from first_app import db

revision = 'e08764c7ec5e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'books',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('title', db.String(100), nullable=False),
        db.Column('author', db.String(100), nullable=False),
        db.Column('description', db.Text, nullable=False),
        db.Column('genres', db.String(100))
    )

    op.create_table(
        'users',
        db.Column('id', db.Integer, primary_key=True, autoincrement=True),
        db.Column('email', db.String(120), unique=True, nullable=False),
        db.Column('username', db.String(80), unique=True, nullable=False),
        db.Column('password', db.String(500), nullable=False),
        db.Column('gender', db.String(10), nullable=False),
        db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
    )


def downgrade():
    op.drop_table('users')
    op.drop_table('books')
