import click
from flask.cli import with_appcontext
from flask_migrate import upgrade, migrate, init
from app.commands.seed_users import seed_users
from app.commands.seed_roles import seed_roles
from app.commands.seed_permissions import seed_permissions
import os


@click.command("create-db")
@with_appcontext
def create_db():
    """
    Cria o banco, aplica migrações e roda o seed inicial automaticamente.
    """

    migrations_dir = os.path.join(os.getcwd(), "migrations")

    # 1. Se pasta migrations não existir → flask db init
    if not os.path.exists(migrations_dir):
        click.echo("📁 Pasta 'migrations' não encontrada. Inicializando...")
        init()

    # 2. Criar migration
    click.echo("📌 Criando migração inicial...")
    migrate(message="Initial structure")

    # 3. Aplicar migrações
    click.echo("🚀 Aplicando migrações no banco...")
    upgrade()

    # 4. Executar seed
    click.echo("🌱 Executando seed inicial...")

    seed_permissions.callback()
    seed_roles.callback()
    seed_users.callback()

    click.echo("✅ Banco criado, migrado e seed executado com sucesso!")
