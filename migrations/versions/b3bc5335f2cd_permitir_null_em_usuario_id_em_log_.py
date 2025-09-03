"""Permitir NULL em usuario_id em log_sistema

Revision ID: b3bc5335f2cd
Revises: 3eccc08b0e1a
Create Date: 2025-08-14 14:55:01.640626
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b3bc5335f2cd'
down_revision = '3eccc08b0e1a'
branch_labels = None
depends_on = None

def upgrade():
    # Alterações existentes
    with op.batch_alter_table('manutencao', schema=None) as batch_op:
        batch_op.alter_column('tipo',
            existing_type=sa.TEXT(),
            type_=sa.String(length=50),
            existing_nullable=False,
            existing_server_default=sa.text("'GERAL'"))

    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column('usuario',
            existing_type=sa.VARCHAR(length=50),
            nullable=True)

    with op.batch_alter_table('veiculo', schema=None) as batch_op:
        batch_op.drop_column('data_proxima_calibragem')

    # ✅ Correção: permitir NULL em usuario_id
    with op.batch_alter_table('log_sistema', schema=None) as batch_op:
        batch_op.alter_column('usuario_id',
            existing_type=sa.Integer(),
            nullable=True)

def downgrade():
    # Reverter alterações
    with op.batch_alter_table('veiculo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_proxima_calibragem', sa.DATE(), nullable=True))

    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column('usuario',
            existing_type=sa.VARCHAR(length=50),
            nullable=False)

    with op.batch_alter_table('manutencao', schema=None) as batch_op:
        batch_op.alter_column('tipo',
            existing_type=sa.String(length=50),
            type_=sa.TEXT(),
            existing_nullable=False,
            existing_server_default=sa.text("'GERAL'"))

    # ❌ Reverter a permissão de NULL em usuario_id
    with op.batch_alter_table('log_sistema', schema=None) as batch_op:
        batch_op.alter_column('usuario_id',
            existing_type=sa.Integer(),
            nullable=False)
