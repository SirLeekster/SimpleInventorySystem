'''from backend.database import db


class Inventory_Item(db.Model):
    __tablename__ = 'inventory'

    item_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    restock_threshold = db.Column(db.Integer, nullable=False, default=10)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    created_by = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.organization_id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    last_updated = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
'''
from backend.database import db

class Inventory_Item(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='General')
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    created_by = db.Column(db.BigInteger, db.ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.organization_id', ondelete='CASCADE'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    last_updated = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
