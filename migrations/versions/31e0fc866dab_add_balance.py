"""add balance

Revision ID: 31e0fc866dab
Revises: 
Create Date: 2023-11-19 18:32:30.574854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31e0fc866dab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_model', schema=None) as batch_op:
        batch_op.drop_column('balance')

    # ### end Alembic commands ###
