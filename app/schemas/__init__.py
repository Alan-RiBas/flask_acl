from flask import Blueprint

schema_bp = Blueprint("schemas", __name__, url_prefix="/schemas")

from .user_schemas import *
from .auth_schemas import *
from .permission_schemas import *
from .role_schemas import *