import click
from flask.cli import with_appcontext
from extensions import db
from app.models.user import User
from app.models.role import Role
from werkzeug.security import generate_password_hash


@click.command("seed-users")
@with_appcontext
def seed_users():
    """
    Cria usuários de teste adicionais.
    """

    click.echo("👤 Criando usuários de teste...")

    role = Role.query.filter_by(name="admin").first()

    users = [
        ("admin@admin.com", "Admin@123", "Alan Admin"),
        ("maria@example.com", "123456aaa", "Maria Admin"),
    ]

    for email, pwd, name in users:
        if not User.query.filter_by(email=email).first():
            user = User(
                email=email,
                name=name,
                password=generate_password_hash(pwd),
                is_active=True
            )
            user.roles.append(role)
            db.session.add(user)

    db.session.commit()

    click.echo("✅ Usuários criados!")
