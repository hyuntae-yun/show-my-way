"""empty message

Revision ID: bfd33d5f77e3
Revises: 342dd26b7e11
Create Date: 2020-12-03 22:54:01.182161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfd33d5f77e3'
down_revision = '342dd26b7e11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('traindata_g_id_fkey', 'traindata', type_='foreignkey')
    op.create_foreign_key(None, 'traindata', 'users', ['g_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'traindata', type_='foreignkey')
    op.create_foreign_key('traindata_g_id_fkey', 'traindata', 'point_group', ['g_id'], ['id'])
    # ### end Alembic commands ###
