"""created new model

Revision ID: 982ee81a6f3f
Revises: f6d8609209ad
Create Date: 2024-11-05 20:40:26.843242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '982ee81a6f3f'
down_revision = 'f6d8609209ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###
