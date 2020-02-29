"""add ver_code delete email_is_validate

Revision ID: add04409cbf7
Revises: c36d30b2433a
Create Date: 2020-02-29 11:45:38.780484

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'add04409cbf7'
down_revision = 'c36d30b2433a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tag', 'picture',
               existing_type=mysql.VARCHAR(length=255),
               comment=None,
               existing_comment='图片链接',
               existing_nullable=True)
    op.add_column('user', sa.Column('ver_code', sa.Integer(), nullable=True))
    op.alter_column('user', 'is_active',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.drop_column('user', 'email_is_validate')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email_is_validate', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.alter_column('user', 'is_active',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.drop_column('user', 'ver_code')
    op.alter_column('tag', 'picture',
               existing_type=mysql.VARCHAR(length=255),
               comment='图片链接',
               existing_nullable=True)
    # ### end Alembic commands ###
