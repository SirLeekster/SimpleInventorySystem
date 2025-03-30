from backend.models.inventory_item import Inventory_Item
from backend.database import db

# Get all items for an organization
def get_items_for_org(organization_id):
    return Inventory_Item.query.filter_by(organization_id=organization_id).all()

# Optional: Add item to DB (already used in your create_inventory_item route)
def add_inventory_item_to_db(data, user):
    try:
        new_item = Inventory_Item(
            product_name=data["product_name"],
            description=data.get("description", ""),
            category=data.get("category", "General"),
            quantity=data["quantity"],
            price=data["price"],
            created_by=user.user_id,
            organization_id=user.organization_id
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item
    except Exception as e:
        print("Error adding inventory item:", e)
        return None

