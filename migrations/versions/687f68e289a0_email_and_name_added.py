"""email and name added

Revision ID: 687f68e289a0
Revises: 
Create Date: 2025-02-20 22:26:43.001061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '687f68e289a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=False))
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.create_unique_constraint('email_contraint', ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('password',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.drop_column('email')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
