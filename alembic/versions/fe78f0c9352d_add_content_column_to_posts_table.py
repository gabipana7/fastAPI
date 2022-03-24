"""add content column to posts table

Revision ID: fe78f0c9352d
Revises: 2020a3a28f96
Create Date: 2022-03-24 13:08:55.052634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe78f0c9352d'
down_revision = '2020a3a28f96'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
