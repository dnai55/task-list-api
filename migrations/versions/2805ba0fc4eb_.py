"""empty message

Revision ID: 2805ba0fc4eb
Revises: 218e33e096dc
Create Date: 2023-05-09 13:14:52.151858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2805ba0fc4eb'
down_revision = '218e33e096dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###
