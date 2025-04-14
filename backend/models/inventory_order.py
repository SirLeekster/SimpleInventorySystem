from backend.database import db

class InventoryOrder(db.Model):
    __tablename__ = 'inventory_orders'

    order_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(255), nullable=False)
    supplier_id = db.Column(db.BigInteger, db.ForeignKey('suppliers.supplier_id', ondelete='SET NULL'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, fulfilled, cancelled

    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    # Optional relationship if you want to join in queries
    supplier = db.relationship('Supplier', backref='orders', lazy=True)
