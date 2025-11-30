from flask_restx import fields
from extensions import api

user_ns = api.namespace("user", description="User Endpoints")

user_model = user_ns.model("User", {
    "id": fields.Integer,
    "name": fields.String(required=True),
    "email": fields.String(required=True),
    "roles": fields.String(description="Role name")
})

create_user_model = user_ns.model("CreateUser", {
    "name": fields.String(required=True, description="The user's name"),
    "email": fields.String(required=True, description="The user's email"),
    "password": fields.String(required=True, description="The user's password"),
    "roles": fields.List(fields.String, default=["user"], description="List of role names")
})

update_user_model = user_ns.model("UpdateUser", {
    "name": fields.String(description="The user's name"),
    "email": fields.String(description="The user's email"),
    "password": fields.String(description="The user's password"),
    "roles": fields.List(fields.String, description="List of role names")
})

token_response = user_ns.model("TokenResponse", {
    "access_token": fields.String,
    "user": fields.Nested(user_model)
})

error_model = user_ns.model("Error", {
    "error": fields.String
})
