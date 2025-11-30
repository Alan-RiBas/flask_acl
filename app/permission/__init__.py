from flask import Blueprint
    
permission_bp = Blueprint("permission", __name__, url_prefix="/permission")

from .routes import *
from .schemas import *
from .permission_services import *