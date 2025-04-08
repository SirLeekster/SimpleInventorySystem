from backend.database import db
from datetime import datetime

class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    sku_id = db.Column(db.BigInteger, db.ForeignKey('inventory_skus.sku_id'), nullable=False)  # ✅
    organization_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    sold_at = db.Column(db.DateTime, default=datetime.utcnow)
