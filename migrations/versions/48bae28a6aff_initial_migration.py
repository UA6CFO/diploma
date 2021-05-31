"""Initial migration.

Revision ID: 48bae28a6aff
Revises: 
Create Date: 2021-05-09 12:57:22.814158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48bae28a6aff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auto', sa.Column('transm', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('auto', 'transm')
    # ### end Alembic commands ###
