from flask_restx import fields
from extensions import api
    
permission_ns = api.namespace("permission", description="Permission Endpoints")

permission_model = permission_ns.model("Permission", {
    "id": fields.Integer,
    "name": fields.String(required=True)
})

create_permission_model = permission_ns.model("CreatePermission", {
    "name": fields.String(required=True, description="The permission's name"),
})

update_permission_model = permission_ns.model("UpdateRole", {
    "name": fields.String(description="The role's name"),
})

token_response = permission_ns.model("TokenResponse", {
    "access_token": fields.String,
    "role": fields.Nested(permission_model)
})

error_model = permission_ns.model("Error", {
    "error": fields.String
})
