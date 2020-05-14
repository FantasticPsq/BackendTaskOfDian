"""empty message

Revision ID: 8ec3bde213f6
Revises: 
Create Date: 2020-05-14 14:18:37.437238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ec3bde213f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('_password', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=25), nullable=False),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article',
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article')
    op.drop_table('user')
    # ### end Alembic commands ###