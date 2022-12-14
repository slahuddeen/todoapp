"""empty message

Revision ID: 9855c20bf4a7
Revises: 
Create Date: 2022-10-26 12:01:22.653163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9855c20bf4a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('list_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'todos', 'todolists', ['list_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.drop_column('todos', 'list_id')
    # ### end Alembic commands ###
