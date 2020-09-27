"""rename groupID to roleID

Revision ID: 7915cfe0ac09
Revises: 37e43585b228
Create Date: 2020-09-27 18:57:45.115854

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7915cfe0ac09'
down_revision = '37e43585b228'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('roleID', sa.Integer(), nullable=True))
    op.drop_column('games', 'groupID')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('groupID', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('games', 'roleID')
    # ### end Alembic commands ###
