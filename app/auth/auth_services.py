
from flask import request, current_app
from extensions import db
from app.models import User
import jwt, datetime

class AuthService:

    @staticmethod
    def get_me():
        auth = request.headers.get("Authorization", "")
        token = auth.split(" ")[1] if " " in auth else auth
        payload = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
        user = User.query.get(payload["sub"])
        return user.as_dict(), 200
    
    @staticmethod
    def login(data):
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return {"error": "invalid_credentials"}, 401

        payload = {
            "sub": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        }
        token = jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")

        return {
            "access_token": token,
            "user": user.as_dict()
        }, 200