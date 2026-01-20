from flask_restx import Resource
from app.schemas.role_schemas import role_ns, role_model, create_role_model, update_role_model, error_model
from ..decorators import require_permission
from app.services.role_services import RoleService


@role_ns.route('')
class RoleListResource(Resource):
    @role_ns.doc('list_roles')
    @role_ns.marshal_list_with(role_model, code=200, description="Success")
    @role_ns.response(401, "Invalid or expired token", error_model)
    @role_ns.response(403, "Forbidden", error_model)
    @role_ns.response(400, "Bad Request", error_model)
    @require_permission('view_roles')
    def get(self):
        try:
            return RoleService.get_all()
        except Exception as e:
            role_ns.abort(400, str(e))
    
    @role_ns.doc('create_role')
    @role_ns.expect(create_role_model, validate=True)
    @role_ns.response(201, "Role Created", role_model)
    @role_ns.response(401, "Invalid or expired token", error_model)
    @role_ns.response(403, "Forbidden", error_model)
    @role_ns.response(400, "Bad Request", error_model)
    @require_permission('create_role')
    def post(self):
        try:
            data = role_ns.payload or {}
            r = RoleService.create(data.get('name'))
            return {'id': r.id, 'name': r.name}, 201
        except Exception as e:
            role_ns.abort(400, str(e))

@role_ns.route('/<int:role_id>')
@role_ns.param('role_id', 'The Role identifier')
class RoleResource(Resource):
    
    @role_ns.doc('edit_role')
    @role_ns.expect(update_role_model, validate=True)
    @role_ns.response(200, "Role Updated", role_model)
    @role_ns.response(401, "Invalid or expired token", error_model)
    @role_ns.response(403, "Forbidden", error_model)
    @role_ns.response(400, "Bad Request", error_model)
    @role_ns.response(404, "Role not found", error_model)
    @require_permission('edit_role')
    def put(self, role_id):
        try:
            data = role_ns.payload or {}
            RoleService.update(role_id, data.get('name'))
        except Exception as e:
            role_ns.abort(400, str(e))
    
    @role_ns.doc('delete_role')
    @role_ns.response(200, "Role deleted")
    @role_ns.response(401, "Invalid or expired token", error_model)
    @role_ns.response(403, "Forbidden", error_model)
    @role_ns.response(400, "Bad Request", error_model)
    @role_ns.response(404, "Role not found", error_model)
    @require_permission('delete_role')
    def delete(self, role_id):
        try:
            RoleService.delete(role_id)
            return {'message': 'role_deleted'}, 200
        except Exception as e:
            role_ns.abort(400, str(e))