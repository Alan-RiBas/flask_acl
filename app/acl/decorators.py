from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.models import User




def get_current_user():
    auth = request.headers.get('Authorization')
    if not auth:
        return None
    token = auth.split()[-1]
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        return User.query.get(payload['sub'])
    except Exception:
        return None




def require_permission(permission_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({'error': 'not_authenticated'}), 401
            if not user.has_permission(permission_name):
                return jsonify({'error': 'forbidden'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator