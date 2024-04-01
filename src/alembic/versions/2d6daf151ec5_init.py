"""init

Revision ID: 2d6daf151ec5
Revises: 
Create Date: 2024-04-01 16:08:28.426250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d6daf151ec5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agents',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('photo', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meetings',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('participants', sa.JSON(), nullable=False),
    sa.Column('location_lon', sa.FLOAT(), nullable=False),
    sa.Column('location_lat', sa.FLOAT(), nullable=False),
    sa.Column('location_name', sa.String(), nullable=False),
    sa.Column('is_canceled', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('routes',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('locations', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('routes')
    op.drop_table('meetings')
    op.drop_table('agents')
    # ### end Alembic commands ###