from flask_restx import fields
from extensions import api

role_ns = api.namespace("role", description="Role Endpoints")

role_model = role_ns.model("Role", {
    "id": fields.Integer,
    "name": fields.String(required=True)
})

create_role_model = role_ns.model("CreateRole", {
    "name": fields.String(required=True, description="The role's name"),
})

update_role_model = role_ns.model("UpdateRole", {
    "name": fields.String(description="The role's name"),
})

token_response = role_ns.model("TokenResponse", {
    "access_token": fields.String,
    "role": fields.Nested(role_model)
})

error_model = role_ns.model("Error", {
    "error": fields.String
})
