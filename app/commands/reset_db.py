import os
import shutil
import click
from flask.cli import with_appcontext
from extensions import db
from flask_migrate import init, migrate, upgrade
from sqlalchemy import create_engine, text


@click.command("reset-db")
@with_appcontext
def reset_db():
    """
    Reseta COMPLETAMENTE o banco:
    - Apaga banco MySQL ou arquivo SQLite
    - Remove pasta migrations
    - Recria migrations
    - Executa upgrade
    - Executa seed inicial
    """

    click.echo("⚠️  Resetando banco COMPLETAMENTE...")

    engine = db.engine
    url = engine.url
    dialect = url.get_dialect().name
    database_name = url.database

    # -------------------------------------------------------------------
    # 1. MYSQL → DROPAR E RECRIAR BANCO
    # -------------------------------------------------------------------
    if dialect == "mysql":
        click.echo(f"🗑️  Deletando e recriando banco MySQL: {database_name}")

        # Criar engine sem selecionar database
        root_url = url.set(database=None)
        root_engine = create_engine(root_url)

        # Drop + Create
        with root_engine.connect() as conn:
            conn.execute(text(f"DROP DATABASE IF EXISTS `{database_name}`;"))
            conn.execute(text(
                f"CREATE DATABASE `{database_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            ))

        root_engine.dispose()
        engine.dispose()

        click.echo("✅ Banco MySQL recriado com sucesso!")

    # -------------------------------------------------------------------
    # 2. SQLITE → APAGAR ARQUIVO
    # -------------------------------------------------------------------
    elif dialect == "sqlite":
        if os.path.exists(database_name):
            click.echo(f"🗑️  Removendo arquivo SQLite: {database_name}")
            os.remove(database_name)

    else:
        click.echo(f"❌ Dialeto não suportado: {dialect}")
        return

    # -------------------------------------------------------------------
    # 3. REMOVER migrations/ PARA RECRIAR DO ZERO
    # -------------------------------------------------------------------
    migrations_dir = os.path.join(os.getcwd(), "migrations")

    if os.path.exists(migrations_dir):
        click.echo("🗑️  Removendo pasta migrations...")
        shutil.rmtree(migrations_dir)

    # -------------------------------------------------------------------
    # 4. RECRIAR MIGRATIONS
    # -------------------------------------------------------------------
    click.echo("📁 Criando pasta migrations...")
    init()

    click.echo("📌 Criando migration inicial...")
    migrate(message="Initial")

    click.echo("🚀 Aplicando migrações...")
    upgrade()

    # -------------------------------------------------------------------
    # 5. EXECUTAR SEED INICIAL
    # -------------------------------------------------------------------
    click.echo("🌱 Executando seed inicial...")

    from app.commands.create_db import create_db
    create_db.callback()

    click.echo("🎉 Banco resetado com sucesso!")
