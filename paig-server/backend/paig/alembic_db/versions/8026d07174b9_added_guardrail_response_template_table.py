"""added guardrail response template table

Revision ID: 8026d07174b9
Revises: 22d276af0074
Create Date: 2024-12-03 18:39:57.191056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import core.db_models.utils


# revision identifiers, used by Alembic.
revision: str = '8026d07174b9'
down_revision: Union[str, None] = '22d276af0074'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('response_template',
    sa.Column('response', sa.String(length=4000), nullable=False),
    sa.Column('description', sa.String(length=4000), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_response_template_create_time'), 'response_template', ['create_time'], unique=False)
    op.create_index(op.f('ix_response_template_id'), 'response_template', ['id'], unique=False)
    op.create_index(op.f('ix_response_template_update_time'), 'response_template', ['update_time'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_response_template_update_time'), table_name='response_template')
    op.drop_index(op.f('ix_response_template_id'), table_name='response_template')
    op.drop_index(op.f('ix_response_template_create_time'), table_name='response_template')
    op.drop_table('response_template')
    # ### end Alembic commands ###