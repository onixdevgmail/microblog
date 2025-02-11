"""empty message

Revision ID: 2b543f39b332
Revises: 99e858d03cf2
Create Date: 2020-05-05 15:30:49.372985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b543f39b332'
down_revision = '99e858d03cf2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'body',
               existing_type=sa.VARCHAR(length=140),
               type_=sa.String(length=10000),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'body',
               existing_type=sa.String(length=10000),
               type_=sa.VARCHAR(length=140),
               existing_nullable=True)
    # ### end Alembic commands ###
