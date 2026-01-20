from extensions import db
from app.models import User, Role

class UserService:

    @staticmethod
    def list_users():
        users = User.query.all()
        return [user.as_dict() for user in users]
    
    @staticmethod
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return user.as_dict()
    
    @staticmethod
    def create_user(data):
        if User.query.filter_by(email=data.get('email')).first():
            return {'error': 'Email already exists'}, 400
        role_names = data.get('roles', []) or []
        roles = Role.query.filter(Role.name.in_(role_names)).all()
        user = User(name=data.get('name'), email=data.get('email'), roles=roles)
    
        user.set_password(data.get('password', 'changeme'))
        db.session.add(user)
        db.session.commit()
        return {'message': 'user_created'}, 201
    
    @staticmethod
    def edit_user(user_id: str, data):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        if "name" in data:
            user.name = data["name"]
        if "password" in data:
            user.set_password(data["password"])
        if "roles" in data:
            role_names = data["roles"] or []
            roles = Role.query.filter(Role.name.in_(role_names)).all()
            user.roles = roles

        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'user_deleted'}, 200