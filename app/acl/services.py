from extensions import db
from app.models import User, Role, Permission

def create_role(name):
    r = Role(name=name)
    db.session.add(r)
    db.session.commit()
    return r

def create_permission(name):
    p = Permission(name=name)
    db.session.add(p)
    db.session.commit()
    return p

def assign_role_to_user(user: User, role: Role):
    user.roles.append(role)
    db.session.commit()

def add_permission_to_role(role: Role, perm: Permission):
    role.permissions.append(perm)
    db.session.commit()