from app.decorators import require_permission
from flask import request, current_app
from flask_restx import Resource
from .schemas import auth_ns, login_model, token_response, error_model, user_model
from .auth_services import AuthService

@auth_ns.route("/login")
class LoginResource(Resource):

    @auth_ns.expect(login_model)
    @auth_ns.response(200, "Success", token_response)
    @auth_ns.response(401, "Invalid Credentials", error_model)

    def post(self):
        try:
            data = request.json or {}
            return AuthService.login(data)
        except Exception:
            return {"error": "invalid_request"}, 400


@auth_ns.route("/me")
class MeResource(Resource):

    @require_permission('view_user')
    @auth_ns.response(200, "Success", user_model)
    @auth_ns.response(401, "Invalid or expired token", error_model)
    @auth_ns.response(404, "User not found", error_model)
    @auth_ns.response(400, "Missing token", error_model)
    def get(self):
        try:
            return AuthService.get_me()
        except Exception:
            return {"error": "invalid_token"}, 401
