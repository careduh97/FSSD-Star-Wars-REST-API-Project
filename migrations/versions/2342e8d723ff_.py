"""empty message

Revision ID: 2342e8d723ff
Revises: fcceeb01f067
Create Date: 2023-03-30 01:51:06.062411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2342e8d723ff'
down_revision = 'fcceeb01f067'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('favorites_planet_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorites_character_id_fkey', type_='foreignkey')
        batch_op.drop_column('planet_id')
        batch_op.drop_column('character_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('favorites_character_id_fkey', 'character', ['character_id'], ['id'])
        batch_op.create_foreign_key('favorites_planet_id_fkey', 'planet', ['planet_id'], ['id'])
        batch_op.drop_column('type_id')

    # ### end Alembic commands ###
