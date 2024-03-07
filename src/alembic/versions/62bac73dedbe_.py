"""empty message

Revision ID: 62bac73dedbe
Revises: f312fc51072d
Create Date: 2024-03-06 12:27:30.145733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62bac73dedbe'
down_revision: Union[str, None] = 'f312fc51072d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id_user', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('login', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('banned', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id_user'),
    sa.UniqueConstraint('login')
    )
    op.drop_table('group')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id_user', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('login', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('banned', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id_user', name='group_pkey'),
    sa.UniqueConstraint('login', name='group_login_key')
    )
    op.drop_table('user')
    # ### end Alembic commands ###