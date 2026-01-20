from app.models.permission import Permission
from extensions import db
from app.models import Role

class RoleService:
    
    @staticmethod
    def create(name, permissions=None):
        name = name.replace(" ", "_").lower()

        if Role.query.filter_by(name=name).first():
            raise ValueError("Role with this name already exists.")
        if not permissions:
            permissions = []
        normalized_permissions = [
            p.replace(" ", "_").lower()
            for p in permissions
        ]

        perms = Permission.query.filter(
            Permission.name.in_(normalized_permissions)
        ).all()

        role = Role(name=name)
        role.permissions = perms

        db.session.add(role)
        db.session.commit()

        return role

    @staticmethod
    def get_all():
        roles = Role.query.all()
        return [role.as_dict() for role in roles]
    
    @staticmethod
    def get_by_id(role_id):
        role = Role.query.get(role_id)
        if role is None:
            raise ValueError("Role not found.")
        return { **role.as_dict() }
    
    @staticmethod
    def update(role_id, name, permissions=None):
        if permissions is None:
            permissions = []
        normalized_permissions = [
            p.replace(" ", "_").lower()
            for p in permissions
        ]
        perms = Permission.query.filter(
            Permission.name.in_(normalized_permissions)
        ).all()

        role = Role.query.get(role_id)
        if role is None:
            raise ValueError("Role not found.")
        role.name = name.replace(" ", "_").lower()
        role.permissions = perms
        db.session.commit()
        return role
    
    @staticmethod
    def delete(role_id):
        role = Role.query.get(role_id)
        if role:
            db.session.delete(role)
            db.session.commit()
        return role