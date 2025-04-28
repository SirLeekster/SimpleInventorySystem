from backend.database import db

"""
this class defines the inventory_skus table using sqlalchemy orm.
"""

class InventorySKU(db.Model):
    __tablename__ = 'inventory_skus'

    sku_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id', ondelete='CASCADE'), nullable=False)
    sku_code = db.Column(db.String(100), unique=True, nullable=False)
    serial_number = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='in_stock')  # e.g., in_stock, sold, damaged
    expiration_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

