from flask_restx import Resource
from app.schemas.permission_schemas import permission_ns, permission_model, create_permission_model, update_permission_model, error_model
from ..decorators import require_permission
from app.services.permission_services import PermissionService


@permission_ns.route('')
class PermissionListResource(Resource):
    @permission_ns.doc('list_permissions')
    @permission_ns.marshal_list_with(permission_model, code=200, description="Success")
    @permission_ns.response(401, "Invalid or expired token", error_model)
    @permission_ns.response(403, "Forbidden", error_model)
    @permission_ns.response(400, "Bad Request", error_model)
    @require_permission('view_permissions')
    def get(self):
        try:
            return PermissionService.get_all()
        except Exception as e:
            permission_ns.abort(400, str(e))
    
    @permission_ns.doc('create_permission')
    @permission_ns.expect(create_permission_model, validate=True)
    @permission_ns.response(201, "Permission created", permission_model)
    @permission_ns.response(401, "Invalid or expired token", error_model)
    @permission_ns.response(403, "Forbidden", error_model)
    @permission_ns.response(400, "Bad Request", error_model)
    @require_permission('create_permission')
    def post(self):
        try:
            data = permission_ns.payload or {}
            r = PermissionService.create(data.get('name'))
            return {'id': r.id, 'name': r.name}, 201
        except Exception as e:
            permission_ns.abort(400, str(e))

@permission_ns.route('/<int:permission_id>')
@permission_ns.param('permission_id', 'The Permission identifier')
class PermissionResource(Resource):
    
    @permission_ns.doc('edit_permission')
    @permission_ns.expect(update_permission_model, validate=True)
    @permission_ns.marshal_with(permission_model, code=200, description="Permission updated")
    @permission_ns.response(401, "Invalid or expired token", error_model)
    @permission_ns.response(403, "Forbidden", error_model)
    @permission_ns.response(400, "Bad Request", error_model)
    @permission_ns.response(404, "Permission not found", error_model)
    @require_permission('edit_permission')
    def put(self, permission_id):
        try:
            data = permission_ns.payload or {}
            PermissionService.update(permission_id, data.get('name'))
        except Exception as e:
            permission_ns.abort(400, str(e))
    
    @permission_ns.doc('delete_role')
    @permission_ns.response(200, "Role deleted")
    @permission_ns.response(401, "Invalid or expired token", error_model)
    @permission_ns.response(403, "Forbidden", error_model)
    @permission_ns.response(400, "Bad Request", error_model)
    @permission_ns.response(404, "Role not found", error_model)
    @require_permission('delete_role')
    def delete(self, permission_id):
        try:
            PermissionService.delete(permission_id)
            return {'message': 'permission_deleted'}, 200
        except Exception as e:
            permission_ns.abort(400, str(e))