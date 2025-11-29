import click
from flask.cli import with_appcontext
from extensions import db
from app.models.permission import Permission


@click.command("seed-permissions")
@with_appcontext
def seed_permissions():
    """
    Adiciona permissões extras ao sistema.
    """

    click.echo("🔐 Criando permissões adicionais...")

    extra_permissions = [
        "dashboard.view",
        "settings.update",
        "logs.view",
        "view_users",
        "view_user",
        "create_user",
        "edit_user",
        "delete_user",
        "view_roles",
        "create_role",
        "edit_role",
        "delete_role",
        "view_permissions",
        "create_permission",
        "edit_permission",
        "delete_permission"
    ]

    for p in extra_permissions:
        if not Permission.query.filter_by(name=p).first():
            perm = Permission(name=p)
            db.session.add(perm)

    db.session.commit()

    click.echo("✅ Permissões adicionais criadas!")
