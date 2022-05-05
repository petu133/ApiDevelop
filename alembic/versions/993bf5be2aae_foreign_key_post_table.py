"""foreign key -> post table

Revision ID: 993bf5be2aae
Revises: 45525821fc34
Create Date: 2022-05-04 21:27:54.316709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '993bf5be2aae'
down_revision = '45525821fc34'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('id_owner', sa.Integer(), nullable = False))
    op.create_foreign_key('link_post_to_user', source_table="posts", referent_table="users",
    local_cols=['id_owner'], remote_cols=['id'], ondelete="CASCADE")#Set foreign key constraint that links the tables. 
    pass


def downgrade():
    op.drop_constraint('link_post_to_user', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
