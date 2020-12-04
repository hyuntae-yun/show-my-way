"""empty message

Revision ID: 9e6a094614b6
Revises: 3c667a0d9532
Create Date: 2020-12-04 01:22:41.245534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e6a094614b6'
down_revision = '3c667a0d9532'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('traindata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('u_id', sa.Integer(), nullable=True),
    sa.Column('X', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['u_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('traindata')
    # ### end Alembic commands ###
