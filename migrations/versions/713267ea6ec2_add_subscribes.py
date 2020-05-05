"""Add Subscribes

Revision ID: 713267ea6ec2
Revises: 0aa93eeff5fd
Create Date: 2020-04-23 16:26:07.810460

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '713267ea6ec2'
down_revision = '0aa93eeff5fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('subscribe_user_id_fkey', 'subscribe', type_='foreignkey')
    op.drop_column('subscribe', 'life_time')
    op.drop_column('subscribe', 'user_id')
    op.add_column('user', sa.Column('subs_expiration', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('subs_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'subscribe', ['subs_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'subs_id')
    op.drop_column('user', 'subs_expiration')
    op.add_column('subscribe', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('subscribe', sa.Column('life_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.create_foreign_key('subscribe_user_id_fkey', 'subscribe', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###
