from extensions import db




class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    permissions = db.relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles"
    )
    users = db.relationship(
        'User', 
        secondary='user_roles', 
        back_populates='roles'
    )

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "permissions": [permission.name for permission in self.permissions]
        }

    def __repr__(self):
        return f"<Role(name={self.name})>"