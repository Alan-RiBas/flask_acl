
from flask import request, current_app
from extensions import db
from app.models import User
# import jwt, datetime
from app.utils.token_generate import generate_token, decode_token

class AuthService:

    @staticmethod
    def get_me():
        payload = (decode_token(request.headers.get("Authorization", "").split(" ")[1]))
        user = User.query.get(payload["sub"])
        if not user:
            return {"error": "user_not_found"}, 404
        
        userWithPermissions = user.as_dict()
        userWithPermissions["permissions"] = user.get_permissions()
        return userWithPermissions, 200
    
    @staticmethod
    def login(data):
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return {"error": "invalid_credentials"}, 401

        token = generate_token(user.id)
        return {
            "access_token": token,
            "user": user.as_dict()
        }, 200