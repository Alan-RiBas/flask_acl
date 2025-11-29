from extensions import db

role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id")),
)

class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    roles = db.relationship(
        'Role',
        secondary='role_permissions', 
        back_populates='permissions'
    )

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

