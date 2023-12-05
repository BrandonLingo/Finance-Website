"""withdrawl

Revision ID: c1f042daa3b1
Revises: b1c68b02d576
Create Date: 2023-11-21 11:16:19.869847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1f042daa3b1'
down_revision = 'b1c68b02d576'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('withdrawl_content', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_model', schema=None) as batch_op:
        batch_op.drop_column('withdrawl_content')

    # ### end Alembic commands ###
