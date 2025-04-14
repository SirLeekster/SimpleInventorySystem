from backend.database import db
from backend.models.inventory_item import Inventory_Item
from backend.models.inventory_sku import InventorySKU
from backend.models.sale import Sale
from sqlalchemy import func
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename
import os


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

    total_sales = db.session.query(func.coalesce(func.sum(Sale.price), 0.00)).filter_by(
        organization_id=organization_id
    ).scalar()

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
        return new_item  # return the full item
    except Exception as e:
        print("Inventory DB Insert Error:", e)
        db.session.rollback()
        return None


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

def get_items_for_org(organization_id):
    return Inventory_Item.query.filter_by(organization_id=organization_id).all()


def save_inventory_image(item_id, image_file):
    try:
        item = Inventory_Item.query.get(item_id)
        if not item:
            return False, "Item not found"

        filename = secure_filename(image_file.filename)

        # Use the correct upload folder from config
        from config import Config
        upload_dir = Config.UPLOAD_FOLDER
        os.makedirs(upload_dir, exist_ok=True)

        filepath = os.path.join(upload_dir, filename)
        image_file.save(filepath)

        # The URL path (what the browser needs) should point to /static/
        relative_url = f"/static/image_uploads/{filename}"
        item.image_path = relative_url

        db.session.commit()

        return True, relative_url
    except Exception as e:
        db.session.rollback()
        return False, f"Error saving image: {str(e)}"


def get_skus_by_inventory_item(item_id):
    skus = InventorySKU.query.filter_by(inventory_id=item_id).all()
    return [sku.to_dict() for sku in skus]