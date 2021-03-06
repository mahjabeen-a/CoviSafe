"""initial migration

Revision ID: 8c6143777279
Revises: 7bac42ec385e
Create Date: 2021-05-30 19:47:12.240200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c6143777279'
down_revision = '7bac42ec385e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer_order', schema=None) as batch_op:
        batch_op.create_foreign_key('customer_id', 'customer', ['customer_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer_order', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
