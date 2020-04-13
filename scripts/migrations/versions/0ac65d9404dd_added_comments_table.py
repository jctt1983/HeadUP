"""Added comments table

Revision ID: 0ac65d9404dd
Revises: 4a3fe41944bf
Create Date: 2018-04-14 19:54:33.869911

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0ac65d9404dd'
down_revision = '4a3fe41944bf'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.drop_table('comments')
    except:
        pass
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('text', sa.Text(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], onupdate='NO ACTION', ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='NO ACTION', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_collate='utf8mb4_unicode_ci',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB')

    op.alter_column(u'posts', 'lang',
                    existing_type=mysql.VARCHAR(length=4),
                    nullable=False,
                    existing_server_default=sa.text(u"'en'"))

    try:
        op.drop_index('idx_lang', table_name='posts')
    except:
        pass
    try:
        op.drop_index('idx_score', table_name='posts')
    except:
        pass
    try:
        op.drop_index('idx_status', table_name='posts')
    except:
        pass
    try:
        op.drop_index('idx_reset_password', table_name='users')
    except:
        pass

    try:
        op.drop_index(op.f('ix_users_reset_password'), table_name='users')
    except:
        pass
    try:
        op.drop_index(op.f('ix_posts_status'), table_name='posts')
    except:
        pass
    try:
        op.drop_index(op.f('ix_posts_score'), table_name='posts')
    except:
        pass
    try:
        op.drop_index(op.f('ix_posts_lang'), table_name='posts')
    except:
        pass

    op.create_index(op.f('ix_users_reset_password'), 'users', ['reset_password'], unique=True)
    op.create_index(op.f('ix_posts_lang'), 'posts', ['lang'], unique=False)
    op.create_index(op.f('ix_posts_score'), 'posts', ['score'], unique=False)
    op.create_index(op.f('ix_posts_status'), 'posts', ['status'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_reset_password'), table_name='users')
    op.drop_index(op.f('ix_posts_status'), table_name='posts')
    op.drop_index(op.f('ix_posts_score'), table_name='posts')
    op.drop_index(op.f('ix_posts_lang'), table_name='posts')

    op.create_index('idx_reset_password', 'users', ['reset_password'], unique=True)
    op.create_index('idx_status', 'posts', ['status'], unique=False)
    op.create_index('idx_score', 'posts', ['score'], unique=False)
    op.create_index('idx_lang', 'posts', ['lang'], unique=False)

    op.alter_column(u'posts', 'lang',
                    existing_type=mysql.VARCHAR(length=4),
                    nullable=True,
                    existing_server_default=sa.text(u"'en'"))

    op.drop_table('comments')
    # ### end Alembic commands ###
