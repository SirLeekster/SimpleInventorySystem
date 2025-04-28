from backend.database import db

"""
this class defines the user_logs table using sqlalchemy orm.
"""


class UserLog(db.Model):
    __tablename__ = 'user_logs'

    log_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=True)
    action = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())
