"""empty message

Revision ID: 3ebdf735a44c
Revises: 6f1483d5df62
Create Date: 2024-09-23 18:18:58.134929

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3ebdf735a44c'
down_revision = '6f1483d5df62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('carts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('carts_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'products', ['product_id'], ['id'])
        batch_op.drop_column('customer_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('carts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('customer_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('carts_ibfk_1', 'customers', ['customer_id'], ['id'])
        batch_op.drop_column('product_id')

    # ### end Alembic commands ###
