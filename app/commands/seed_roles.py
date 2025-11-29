import click
from flask.cli import with_appcontext
from extensions import db
from app.models import Role
from app.models.permission import Permission


@click.command("seed-roles")
@with_appcontext
def seed_roles():
    """Popula roles iniciais no sistema."""
    roles = [
        {"name": "admin"},
        {"name": "manager"},
        {"name": "user"},
    ]

    for r in roles:
        if not Role.query.filter_by(name=r["name"]).first():
            db.session.add(Role(name=r["name"]))
    
    db.session.commit()

    # 2. Adicionar PERMISSÕES ao ADMIN
    admin_role = Role.query.filter_by(name="admin").first()
    admin_role.permissions = Permission.query.all()
    db.session.add(admin_role)

    # 3. Manager
    manager_role = Role.query.filter_by(name="manager").first()
    manager_permissions = [
        "dashboard.view",
        "logs.view",
        "view_users",
        "view_user",
    ]
    perms = Permission.query.filter(Permission.name.in_(manager_permissions)).all()
    manager_role.permissions = perms
    db.session.add(manager_role)
    
    # 4. User
    user_role = Role.query.filter_by(name="user").first()
    user_permissions = [
        "view_user",
    ]
    perms = Permission.query.filter(Permission.name.in_(user_permissions)).all()
    user_role.permissions = perms
    db.session.add(user_role)

    db.session.commit()
    click.echo("🌱 Roles criadas com sucesso!")
