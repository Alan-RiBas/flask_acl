from flask import request, jsonify
from . import acl_bp
from extensions import db
from app.models import Permission
from .decorators import require_permission
from .services import create_permission

@acl_bp.get('/permissions')
@require_permission('view_permissions')
def list_permissions():
    try:
        perms = Permission.query.order_by(Permission.id).all()
        return jsonify([p.as_dict() for p in perms]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@acl_bp.post('/permissions')
@require_permission('create_permission')
def create_permission_route():
    try:
        data = request.json or {}
        p = create_permission(data.get('name'))
        return jsonify({'id': p.id, 'name': p.name}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@acl_bp.put('/permissions/<int:permission_id>')
@require_permission('edit_permission')
def edit_permission(permission_id):
    try:
        permission = Permission.query.get_or_404(permission_id)
        data = request.json or {}
        permission.name = data.get('name', permission.name)
        db.session.commit()
        return jsonify({'id': permission.id, 'name': permission.name}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@acl_bp.delete('/permissions/<int:permission_id>')
@require_permission('delete_permission')
def delete_permission(permission_id):
    try:
        permission = Permission.query.get_or_404(permission_id)
        db.session.delete(permission)
        db.session.commit()
        return jsonify({'message': 'permission_deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400