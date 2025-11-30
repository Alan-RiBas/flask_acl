from flask_restx import fields
from extensions import api

auth_ns = api.namespace("auth", description="Auth Endpoints")

login_model = auth_ns.model("Login", {
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})

user_model = auth_ns.model("User", {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "roles": fields.String
})

token_response = auth_ns.model("TokenResponse", {
    "access_token": fields.String,
    "user": fields.Nested(user_model)
})

error_model = auth_ns.model("Error", {
    "error": fields.String
})
