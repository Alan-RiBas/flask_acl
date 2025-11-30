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
        user = User(name=data.get('name'), email=data.get('email'))
        user.set_password(data.get('password', 'changeme'))
        db.session.add(user)
        db.session.commit()
        return {'message': 'user_created', 'id': user.id}, 201
    
    @staticmethod
    def edit_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
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