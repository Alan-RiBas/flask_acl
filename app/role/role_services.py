from extensions import db
from app.models import Role

class RoleService:
    
    @staticmethod
    def create_role(name):
        r = Role(name=name)
        db.session.add(r)
        db.session.commit()
        return r
    
    @staticmethod
    def get_all_roles():
        return Role.query.all()
    
    @staticmethod
    def update_role(role_id, name):
        role = Role.query.get(role_id)
        if role:
            role.name = name
            db.session.commit()
        return role
    
    @staticmethod
    def delete_role(role_id):
        role = Role.query.get(role_id)
        if role:
            db.session.delete(role)
            db.session.commit()
        return role