"""start

Revision ID: 8f2ce8739263
Revises:
Create Date: 2018-04-09 18:53:41.924000

"""
from alembic import op
import sqlalchemy as sa
from app.helpers.json.database import DatabaseJSONEncoder


# revision identifiers, used by Alembic.
revision = '8f2ce8739263'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=128), nullable=True),
                    sa.Column('slug', sa.String(length=128), nullable=True),
                    sa.Column('attr', DatabaseJSONEncoder(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_collate='utf8mb4_unicode_ci',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB')
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=True)
    op.create_index(op.f('ix_categories_slug'), 'categories', ['slug'], unique=True)
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=128), nullable=True),
                    sa.Column('password', sa.String(length=128), nullable=True),
                    sa.Column('role_id', sa.Integer(), nullable=True),
                    sa.Column('attr', DatabaseJSONEncoder(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_collate='utf8mb4_unicode_ci',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('pictures',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('attr', DatabaseJSONEncoder(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='NO ACTION', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_collate='utf8mb4_unicode_ci',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB')
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=255), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('category_id', sa.Integer(), nullable=True),
                    sa.Column('status', sa.Integer(), nullable=True),
                    sa.Column('lang', sa.String(length=4), nullable=True),
                    sa.Column('anonymous', sa.SmallInteger(), nullable=True),
                    sa.Column('score', sa.Numeric(precision=20, scale=7), server_default='0', nullable=False),
                    sa.Column('attr', DatabaseJSONEncoder(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], onupdate='NO ACTION', ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='NO ACTION', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_collate='utf8mb4_unicode_ci',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB')
    op.create_index(op.f('ix_posts_lang'), 'posts', ['lang'], unique=False)
    op.create_index(op.f('ix_posts_status'), 'posts', ['status'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_posts_status'), table_name='posts')
    op.drop_index(op.f('ix_posts_lang'), table_name='posts')
    op.drop_table('posts')
    op.drop_table('pictures')
    op.drop_index(op.f('ix_users_reset_password'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_categories_slug'), table_name='categories')
    op.drop_index(op.f('ix_categories_name'), table_name='categories')
    op.drop_table('categories')
    # ### end Alembic commands ###
