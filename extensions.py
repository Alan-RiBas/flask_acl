from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Insert your token like: Bearer <token>"
    }
}

api = Api(
    title="Flask ACL API",
    version="1.0",
    doc="/api",
    description="REST API with JWT Auth",
    authorizations=authorizations,
    security="Bearer",
)

db = SQLAlchemy()
migrate = Migrate()