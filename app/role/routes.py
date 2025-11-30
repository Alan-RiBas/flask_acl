from flask_restx import Resource
from .schemas import role_ns, role_model, create_role_model, update_role_model, error_model
from ..decorators import require_permission
from .role_services import RoleService


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
            return RoleService.get_all_roles()
        except Exception as e:
            role_ns.abort(400, str(e))
    
    @role_ns.doc('create_role')
    @role_ns.expect(create_role_model, validate=True)
    @role_ns.marshal_with(role_model, code=201, description="Role created")
    @role_ns.response(401, "Invalid or expired token", error_model)
    @role_ns.response(403, "Forbidden", error_model)
    @role_ns.response(400, "Bad Request", error_model)
    @require_permission('create_role')
    def post(self):
        try:
            data = role_ns.payload or {}
            r = RoleService.create_role(data.get('name'))
            return {'id': r.id, 'name': r.name}, 201
        except Exception as e:
            role_ns.abort(400, str(e))

@role_ns.route('/<int:role_id>')
class RoleResource(Resource):
    
    @role_ns.doc('edit_role')
    @role_ns.expect(update_role_model, validate=True)
    @role_ns.marshal_with(role_model, code=200, description="Role updated")
    @role_ns.response(401, "Invalid or expired token", error_model)
    @role_ns.response(403, "Forbidden", error_model)
    @role_ns.response(400, "Bad Request", error_model)
    @role_ns.response(404, "Role not found", error_model)
    @require_permission('edit_role')
    def put(self, role_id):
        try:
            data = role_ns.payload or {}
            RoleService.update_role(role_id, data.get('name'))
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
            RoleService.delete_role(role_id)
            return {'message': 'role_deleted'}, 200
        except Exception as e:
            role_ns.abort(400, str(e))

    

    

# @require_permission('view_roles')
# def list_roles():
#     try:
#         roles = Role.query.all()
#         return jsonify([r.as_dict() for r in roles])
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# @acl_bp.post('/roles')
# @require_permission('create_role')
# def create_role_route():
#     try:
#         data = request.json or {}
#         r = create_role(data.get('name'))
#         return jsonify({'id': r.id, 'name': r.name}), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# @acl_bp.put('/roles/<int:role_id>')
# @require_permission('edit_role')
# def edit_role(role_id):
#     try:
#         role = Role.query.get_or_404(role_id)
#         data = request.json or {}
#         role.name = data.get('name', role.name)
#         db.session.commit()
#         return jsonify({'id': role.id, 'name': role.name}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# @acl_bp.delete('/roles/<int:role_id>')
# @require_permission('delete_role')
# def delete_role(role_id):
#     try:
#         role = Role.query.get_or_404(role_id)
#         db.session.delete(role)
#         db.session.commit()
#         return jsonify({'message': 'role_deleted'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400