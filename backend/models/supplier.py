from backend.database import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'

    supplier_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
