from flask import Blueprint

services_bp = Blueprint("services", __name__, url_prefix="/services")

from .user_services import *
from .auth_services import *
from .permission_services import *
from .role_services import *