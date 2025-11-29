from flask import request, jsonify
from . import acl_bp
from extensions import db
from app.models import User, Role, Permission
from .decorators import require_permission
from .services import create_role, create_permission


# USERS
@acl_bp.get('/users')
@require_permission('view_users')
def list_users():
    try:
        users = User.query.all()
        return jsonify([u.as_dict() for u in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@acl_bp.get('/users/<int:user_id>')
@require_permission('view_user')
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.as_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@acl_bp.post('/users')
@require_permission('create_user')
def create_user():
    try:    
        data = request.json or {}
        user = User(name=data.get('name'), email=data.get('email'))
        user.set_password(data.get('password', 'changeme'))
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'user_created', 'id': user.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@acl_bp.put('/users/<int:user_id>')
@require_permission('edit_user')
def edit_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        user = User.query.get_or_404(user_id)
        data = request.json or {}
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return jsonify({'message': 'user_updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@acl_bp.delete('/users/<int:user_id>')
@require_permission('delete_user')
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'user_deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ROLES
@acl_bp.get('/roles')
@require_permission('view_roles')
def list_roles():
    try:
        roles = Role.query.all()
        return jsonify([r.as_dict() for r in roles])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@acl_bp.post('/roles')
@require_permission('create_role')
def create_role_route():
    try:
        data = request.json or {}
        r = create_role(data.get('name'))
        return jsonify({'id': r.id, 'name': r.name}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@acl_bp.put('/roles/<int:role_id>')
@require_permission('edit_role')
def edit_role(role_id):
    try:
        role = Role.query.get_or_404(role_id)
        data = request.json or {}
        role.name = data.get('name', role.name)
        db.session.commit()
        return jsonify({'id': role.id, 'name': role.name}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@acl_bp.delete('/roles/<int:role_id>')
@require_permission('delete_role')
def delete_role(role_id):
    try:
        role = Role.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()
        return jsonify({'message': 'role_deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# PERMISSIONS
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