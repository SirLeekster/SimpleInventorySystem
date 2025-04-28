from backend.database import db

"""
this class defines the users table using sqlalchemy orm.
"""

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.organization_id', ondelete='CASCADE'), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='staff')
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
