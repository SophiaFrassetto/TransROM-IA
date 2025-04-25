"""add password field

Revision ID: c1c6ab94d87d
Revises: 89974dd0be48
Create Date: 2024-03-19 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1c6ab94d87d'
down_revision = '89974dd0be48'
branch_labels = None
depends_on = None


def upgrade():
    # Make google_id nullable
    op.alter_column('users', 'google_id',
               existing_type=sa.String(),
               nullable=True)
    
    # Add password column
    op.add_column('users', sa.Column('password', sa.String(), nullable=True))


def downgrade():
    # Remove password column
    op.drop_column('users', 'password')
    
    # Make google_id non-nullable again
    op.alter_column('users', 'google_id',
               existing_type=sa.String(),
               nullable=False)
