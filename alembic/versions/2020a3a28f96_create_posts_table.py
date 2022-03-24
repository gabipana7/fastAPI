"""create posts table

Revision ID: 2020a3a28f96
Revises: 
Create Date: 2022-03-24 12:57:54.689412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2020a3a28f96'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
                            sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
