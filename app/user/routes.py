from app.models.user import User
from flask import request
from flask_restx import Resource
from ..decorators import require_permission
from .user_services import UserService
from .schemas import user_ns, user_model, create_user_model, update_user_model, error_model


@user_ns.route('')
class UserListResource(Resource):

    @require_permission('view_users')
    @user_ns.marshal_list_with(user_model, code=200, description="Success")
    @user_ns.response(401, "Invalid or expired token", error_model)
    @user_ns.response(403, "Forbidden", error_model)
    @user_ns.response(400, "Bad Request", error_model)
    def get(self):
        try:
            return UserService.list_users()
        except Exception as e:
            return {'error': str(e)}, 400
        
    @require_permission('create_user')
    @user_ns.expect(create_user_model, validate=True)
    @user_ns.response(201, "User Created", user_model)
    @user_ns.response(401, "Invalid or expired token", error_model)
    @user_ns.response(403, "Forbidden", error_model)
    @user_ns.response(400, "Bad Request", error_model)

    def post(self):
        try:
            data = request.json or {}
            return UserService.create_user(data)
        except Exception as e:
            return {'error': str(e)}, 400

@user_ns.route('/<string:user_id>')
@user_ns.param('user_id', 'The User identifier')
class UserResource(Resource):

    @require_permission('view_user')
    @user_ns.marshal_with(user_model, code=200, description="Success")
    @user_ns.response(401, "Invalid or expired token", error_model)
    @user_ns.response(403, "Forbidden", error_model)
    @user_ns.response(400, "Bad Request", error_model)
    def get(self, user_id):
        try:
            return UserService.get_user(user_id)
        except Exception as e:
            return {'error': str(e)}, 400
        
    @require_permission('edit_user')
    @user_ns.expect(update_user_model, validate=True)
    @user_ns.response(200, "User Updated", user_model)
    @user_ns.response(401, "Invalid or expired token", error_model)
    @user_ns.response(403, "Forbidden", error_model)
    @user_ns.response(400, "Bad Request", error_model)
    def put(self, user_id):
        try:
            data = request.json or {}
            return UserService.edit_user(user_id, data)
        except Exception as e:
            return {'error': str(e)}, 400

    @require_permission('delete_user')
    @user_ns.response(200, "User Deleted")
    @user_ns.response(401, "Invalid or expired token", error_model)
    @user_ns.response(403, "Forbidden", error_model)
    @user_ns.response(400, "Bad Request", error_model)
    def delete(self, user_id):
        try:
            return UserService.delete_user(user_id)
        except Exception as e:
            return {'error': str(e)}, 400