import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"
    JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")