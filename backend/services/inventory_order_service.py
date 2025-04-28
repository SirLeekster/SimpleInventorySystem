from backend.models.inventory_order import InventoryOrder
from backend.database import db


# get all inventory orders, ordered by creation date
def get_all_orders() -> list[InventoryOrder]:
    return InventoryOrder.query.order_by(InventoryOrder.created_at.desc()).all()


# get a specific order by id
def get_order_by_id(order_id: int) -> InventoryOrder | None:
    return InventoryOrder.query.get(order_id)


# create a new inventory order
def create_order(item_name: str, quantity: int, supplier_id: int = None, status: str = "pending") -> InventoryOrder:
    order = InventoryOrder(
        item_name=item_name.strip(),
        quantity=quantity,
        supplier_id=supplier_id,
        status=status
    )
    db.session.add(order)
    db.session.commit()
    return order


# update an existing inventory order
def update_order(order_id: int, item_name: str, quantity: int, supplier_id: int = None,
                 status: str = "pending") -> bool:
    order = get_order_by_id(order_id)
    if not order:
        return False

    order.item_name = item_name.strip()
    order.quantity = quantity
    order.supplier_id = supplier_id
    order.status = status

    db.session.commit()
    return True


# delete an inventory order
def delete_order(order_id: int) -> bool:
    order = get_order_by_id(order_id)
    if not order:
        return False
    db.session.delete(order)
    db.session.commit()
    return True
