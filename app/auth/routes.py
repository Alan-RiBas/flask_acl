from flask import request, jsonify, current_app
from . import auth_bp
from app.models import User
import jwt
import datetime


@auth_bp.post('/login')
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')


    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'invalid_credentials'}), 401


    payload = {
        'sub': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')


    return jsonify({
        'access_token': token,
        'user': user.as_dict()
    })


@auth_bp.get('/me')
def me():
    auth = request.headers.get('Authorization')
    if not auth:
        return jsonify({'error': 'missing_token'}), 401
    token = auth.split()[-1]
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        user = User.query.get(payload['sub'])
        if not user:
            return jsonify({'error': 'user_not_found'}), 404
        return jsonify(user.as_dict())
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'token_expired'}), 401
    except Exception:
        return jsonify({'error': 'invalid_token'}), 401