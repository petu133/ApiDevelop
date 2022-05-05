"""add users table

Revision ID: 45525821fc34
Revises: 9f7478c98965
Create Date: 2022-05-03 21:06:33.997257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45525821fc34'
down_revision = '9f7478c98965'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('pw', sa.String(), nullable=False),
                    sa.Column('mail', sa.String(), nullable=False),
                    sa.Column('created', sa.TIMESTAMP(timezone=True),
                    server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('mail')
                    )
    pass

def downgrade():
    op.drop_table('users')
    pass
