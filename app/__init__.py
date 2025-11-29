from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate
from app.commands.create_db import create_db
from app.commands.reset_db import reset_db
from app.commands.seed_users import seed_users
from app.commands.seed_roles import seed_roles
from app.commands.seed_permissions import seed_permissions


# blueprints
from .acl import acl_bp
from .auth import auth_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    cors = CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    # ext
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(acl_bp)
    
    # register commands
    app.cli.add_command(create_db)
    app.cli.add_command(reset_db)
    app.cli.add_command(seed_users)
    app.cli.add_command(seed_roles)
    app.cli.add_command(seed_permissions)

    @app.route("/health")
    def health():
        return {"status": "ok"}


    return app