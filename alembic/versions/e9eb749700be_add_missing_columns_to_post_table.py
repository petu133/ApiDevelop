"""add missing columns to post table

Revision ID: e9eb749700be
Revises: 993bf5be2aae
Create Date: 2022-05-04 22:39:38.846232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9eb749700be'
down_revision = '993bf5be2aae'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable = False, server_default = 'TRUE'))
    op.add_column('posts', sa.Column('creation_time', sa.TIMESTAMP(), nullable = False, server_default = sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'creation_time')
    pass
