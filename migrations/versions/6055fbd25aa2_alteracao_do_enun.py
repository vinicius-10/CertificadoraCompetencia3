"""alteracao do enun

Revision ID: 6055fbd25aa2
Revises: 32257be55206
Create Date: 2026-05-01 13:45:21.316553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6055fbd25aa2'
down_revision = '32257be55206'
branch_labels = None
depends_on = None


def upgrade():
    # Cria o tipo enum no PostgreSQL primeiro
    usermarital = sa.Enum('Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)', 'União Estável',
        name='usermarital')
    usermarital.create(op.get_bind())

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('marital',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.Enum('Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)', 'União Estável',
        name='usermarital'),
               existing_nullable=True,
               postgresql_using="marital::usermarital")


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('marital',
               existing_type=sa.Enum('Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)', 'União Estável',
        name='usermarital'),
               type_=sa.VARCHAR(length=30),
               existing_nullable=True)

    # Remove o tipo enum do PostgreSQL
    sa.Enum(name='usermarital').drop(op.get_bind())