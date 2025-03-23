from backend.database import db

class Inventory_Item(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Inventory {self.product_name} (Qty: {self.quantity})>"
