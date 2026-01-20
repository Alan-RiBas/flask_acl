from extensions import db
from app.models import Role

class RoleService:
    
    @staticmethod
    def create(name):
        # se o nome tiver espaço será incluído um underline
        name = name.replace(" ", "_").lower()
        if Role.query.filter_by(name=name).first():
            raise ValueError("Role with this name already exists.")
        r = Role(name=name)
        db.session.add(r)
        db.session.commit()
        return r
    
    @staticmethod
    def get_all():
        return Role.query.all()
    
    @staticmethod
    def update(role_id, name):
        name = name.replace(" ", "_").lower()
        if Role.query.get_or_404(role_id) is None:
            raise ValueError("Role not found.")
        if Role.query.filter_by(name=name).first():
            raise ValueError("Role with this name already exists.")
        role = Role.query.get(role_id)
        if role:
            role.name = name
            db.session.commit()
        return role
    
    @staticmethod
    def delete(role_id):
        role = Role.query.get(role_id)
        if role:
            db.session.delete(role)
            db.session.commit()
        return role