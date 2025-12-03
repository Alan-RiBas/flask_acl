import uuid
from app.utils.uuid_gen import generate_uuid
from extensions import db

from werkzeug.security import generate_password_hash, check_password_hash

user_roles = db.Table(
    "user_roles",
    db.Column("users_id", db.String(36), db.ForeignKey("users.id"), primary_key=True),
    db.Column("roles_id", db.ForeignKey("roles.id"), primary_key=True),
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, nullable=False)
    name = db.Column(db.String(168), nullable=False)
    email = db.Column(db.String(68), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')

    def as_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "roles": [role.name for role in self.roles]
        }

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_permissions(self):
        perms = set()
        for r in self.roles:
            for p in r.permissions:
                perms.add(p.name)
        return list(perms)


    def has_permission(self, perm_name: str) -> bool:
        return perm_name in self.get_permissions()