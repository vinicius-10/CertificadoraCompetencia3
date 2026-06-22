"""update_user_profile_enum

Revision ID: 575664b036d2
Revises: b0698be47c2d
Create Date: 2026-06-19 18:21:09.988895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '575664b036d2'
down_revision = 'b0698be47c2d'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Renomeia o enum antigo para não dar conflito de nome
    op.execute("ALTER TYPE userprofile RENAME TO userprofile_old")
    
    # 2. Cria o novo enum com a estrutura atualizada (sem ADMIN, com Bolsista)
    new_enum = sa.Enum('Coordenador(a)', 'Bolsista', 'Voluntário(a)', name='userprofile')
    new_enum.create(op.get_bind(), checkfirst=True)
    
    # 3. Atualiza a coluna da tabela 'users' para usar o novo tipo casting os dados antigos
    # Nota: Se algum usuário antigo ainda tiver o valor 'Admin' no banco, o Postgres pode reclamar.
    # Caso tenha usuários com 'Admin', eles precisam ser alterados antes dessa migração rodar.
    op.execute(
        "ALTER TABLE users ALTER COLUMN profile TYPE userprofile USING profile::text::userprofile"
    )
    
    # 4. Apaga o enum antigo que foi renomeado
    op.execute("DROP TYPE userprofile_old")


def downgrade():
    # Para o downgrade, fazemos o processo inverso se precisar voltar atrás
    op.execute("ALTER TYPE userprofile RENAME TO userprofile_old")
    
    old_enum = sa.Enum('Coordenador(a)', 'Admin', 'Voluntário(a)', name='userprofile')
    old_enum.create(op.get_bind(), checkfirst=True)
    
    op.execute(
        "ALTER TABLE users ALTER COLUMN profile TYPE userprofile USING profile::text::userprofile"
    )
    
    op.execute("DROP TYPE userprofile_old")
