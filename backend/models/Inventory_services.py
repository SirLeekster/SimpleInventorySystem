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
