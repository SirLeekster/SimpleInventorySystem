from backend.database import database
from backend.models.inventory_item import Inventory_Item

def get_inventory_from_db():
    inventory_items:list[Inventory_Item] = database.get_inventory_items()

    result = [
        {
            "id": item.id,
            "product_name": item.product_name,
            "quantity": item.quantity,
            "price": item.price,
            "last_updated": item.last_updated.isoformat() if item.last_updated else None
        }
        for item in inventory_items
    ]
    return result

def add_inventory_item_to_db(item_data):
    try:
        new_item = Inventory_Item(
            product_name=item_data['product_name'],
            quantity=item_data['quantity'],
            price=item_data['price']
        )
        database.add_inventory_item(new_item)
        return True
    except Exception as e:
        # Return False if an error occurs
        return False
