from flask import Blueprint

routes_bp = Blueprint("routes", __name__, url_prefix="/api")

from .user_routes import *
from .auth_routes import *
from .permission_routes import *
from .role_routes import *