from flask import Blueprint

role_bp = Blueprint("role", __name__, url_prefix="/role")

from .routes import *
from .schemas import *
from .role_services import *