from flask import Blueprint

acl_bp = Blueprint("acl", __name__, url_prefix="/admin")

from .routes import *