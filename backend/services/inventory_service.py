'''from backend.database import database
from backend.models.inventory_item import Inventory_Item

from backend.database import database
from backend.models.inventory_item import Inventory_Item
from sqlalchemy import func
from datetime import datetime, timedelta

def get_dashboard_stats_for_org(organization_id):
    from backend.database import db

    total_items = db.session.query(func.count(Inventory_Item.item_id)).filter_by(organization_id=organization_id).scalar()

    low_stock = db.session.query(func.count()).filter(
        Inventory_Item.organization_id == organization_id,
        Inventory_Item.quantity > 0,
        Inventory_Item.quantity <= 5
    ).scalar()

    out_of_stock = db.session.query(func.count()).filter(
        Inventory_Item.organization_id == organization_id,
        Inventory_Item.quantity == 0
    ).scalar()

    total_sales = 0.00  # Placeholder for future sales data

    top_item = db.session.query(Inventory_Item.item_name).filter_by(organization_id=organization_id).order_by(Inventory_Item.quantity.desc()).limit(1).scalar()
    top_item = top_item if top_item else "N/A"

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
            item_name=item_data['item_name'],
            sku=item_data['sku'],
            quantity=item_data['quantity'],
            price=item_data['price'],
            created_by=user.user_id,
            organization_id=user.organization_id
        )
        database.add_inventory_item(new_item)
        return True
    except Exception:
        return False
'''

from backend.database import database, db
from backend.models.inventory_item import Inventory_Item
from sqlalchemy import func
from datetime import datetime, timedelta

def get_dashboard_stats_for_org(organization_id):
    total_items = db.session.query(func.count(Inventory_Item.id)).filter(
        Inventory_Item.organization_id == organization_id,
        Inventory_Item.is_active == True
    ).scalar()

    low_stock = db.session.query(func.count()).filter(
        Inventory_Item.organization_id == organization_id,
        Inventory_Item.quantity > 0,
        Inventory_Item.quantity <= 5,
        Inventory_Item.is_active == True
    ).scalar()

    out_of_stock = db.session.query(func.count()).filter(
        Inventory_Item.organization_id == organization_id,
        Inventory_Item.quantity == 0,
        Inventory_Item.is_active == True
    ).scalar()

    total_sales = 0.00  # Placeholder for future sales data

    top_item = db.session.query(Inventory_Item.product_name).filter(
        Inventory_Item.organization_id == organization_id,
        Inventory_Item.is_active == True
    ).order_by(Inventory_Item.quantity.desc()).limit(1).scalar() or "N/A"

    one_week_ago = datetime.utcnow() - timedelta(days=7)
    recent_additions = db.session.query(func.count()).filter(
        Inventory_Item.organization_id == organization_id,
        Inventory_Item.created_at >= one_week_ago,
        Inventory_Item.is_active == True
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
            product_name=item_data['product_name'],  # ✅ FIXED: matches frontend + model
            description=item_data.get('description'),
            category=item_data.get('category', 'General'),
            quantity=item_data['quantity'],
            price=item_data['price'],
            created_by=user.user_id,
            organization_id=user.organization_id
        )
        database.add_inventory_item(new_item)
        return True
    except Exception as e:
        print(f"Error adding inventory item: {e}")
        return False
