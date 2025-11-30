from extensions import db
from app.models import Permission


class PermissionService:
    @staticmethod
    def get_all():
        return Permission.query.all()

    @staticmethod
    def get_by_id(permission_id):
        return Permission.query.get(permission_id)
    
    @staticmethod
    def create(name):
        perm = Permission(name=name)
        db.session.add(perm)
        db.session.commit()
        return perm

    @staticmethod
    def update(permission_id, name):
        perm = PermissionService.get_by_id(permission_id)
        if not perm:
            raise ValueError("Permission not found")
        perm.name = name
        db.session.commit()
        return perm

    @staticmethod
    def delete(permission_id):
        perm = PermissionService.get_by_id(permission_id)
        if not perm:
            raise ValueError("Permission not found")
        db.session.delete(perm)
        db.session.commit()