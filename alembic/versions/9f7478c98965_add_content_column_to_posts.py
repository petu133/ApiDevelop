"""add content column to posts

Revision ID: 9f7478c98965
Revises: d969a8da3d4c
Create Date: 2022-04-23 21:55:28.643446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f7478c98965'
down_revision = 'd969a8da3d4c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
