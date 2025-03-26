from backend.database import db
from backend.models.inventory_item import Inventory_Item
from sqlalchemy import func
from datetime import datetime, timedelta

def get_dashboard_stats_for_org(organization_id):
    total_items = db.session.query(func.count(Inventory_Item.id)).filter_by(
        organization_id=organization_id
    ).scalar()

    low_stock = db.session.query(func.count()).filter(
        Inventory_Item.organization_id == organization_id,
        Inventory_Item.quantity > 0,
        Inventory_Item.quantity <= 5
    ).scalar()

    out_of_stock = db.session.query(func.count()).filter(
        Inventory_Item.organization_id == organization_id,
        Inventory_Item.quantity == 0
    ).scalar()

    total_sales = 0.00  # Placeholder (future implementation)

    top_item = db.session.query(Inventory_Item.product_name).filter_by(
        organization_id=organization_id
    ).order_by(Inventory_Item.quantity.desc()).limit(1).scalar() or "N/A"

    one_week_ago = datetime.utcnow() - timedelta(days=7)
    recent_additions = db.session.query(func.count()).filter(
        Inventory_Item.organization_id == organization_id,
        Inventory_Item.created_at >= one_week_ago
    ).scalar()

    return {
        "total_items": total_items,
        "low_stock_items": low_stock,
        "out_of_stock_items": out_of_stock,
        "total_sales": f"${total_sales:.2f}",
        "top_item": top_item,
        "recent_additions": f"{recent_additions} this week"
    }

def add_inventory_item_to_db(item_data, user):
    try:
        new_item = Inventory_Item(
            product_name=item_data['product_name'],
            description=item_data.get('description', ''),
            category=item_data.get('category', 'General'),
            quantity=item_data['quantity'],
            price=item_data['price'],
            created_by=user.user_id,
            organization_id=user.organization_id
        )
        db.session.add(new_item)
        db.session.commit()
        return True
    except Exception as e:
        print("Inventory DB Insert Error:", e)
        db.session.rollback()
        return False

from fastapi import HTTPException
from backend.models.inventory_item import Inventory_Item
from sqlalchemy.orm import Session

def update_item_quantity(db: Session, item_id: int, change: int):
    item = db.query(Inventory_Item).filter(Inventory_Item.item_id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    new_quantity = item.quantity + change

    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")

    item.quantity = new_quantity
    db.commit()
    db.refresh(item)

    # Optional: Check for low stock
    if item.quantity <= item.restock_threshold:
        print(f"⚠️ Warning: Item '{item.item_name}' is low on stock!")

    return item
