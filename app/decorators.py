from functools import wraps
from flask import request
from app.utils.token_generate import decode_token
from app.models import User

def get_current_user():
    auth = request.headers.get('Authorization')
    if not auth:
        return None

    token = auth.split()[-1]

    try:
        payload = decode_token(token)
        return User.query.get(payload['sub'])
    except Exception:
        return None


def require_permission(permission_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = get_current_user()

            if not user:
                return {'error': 'not_authenticated'}, 401

            if not user.has_permission(permission_name):
                return {'error': 'forbidden'}, 403

            return f(*args, **kwargs)
        return wrapper
    return decorator
