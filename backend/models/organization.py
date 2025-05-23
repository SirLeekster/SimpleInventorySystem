from backend.database import db

"""
this class defines the organizations table using sqlalchemy orm.
"""

class Organization(db.Model):
    __tablename__ = 'organizations'

    organization_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    created_by = db.Column(db.BigInteger, db.ForeignKey('users.user_id', ondelete='SET NULL'))
