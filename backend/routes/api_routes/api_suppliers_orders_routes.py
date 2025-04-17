from flask import Blueprint, request, jsonify, session
from backend.services import supplier_service, inventory_order_service, log_service

api_suppliers_orders_routes = Blueprint("api_suppliers_orders_routes", __name__)

# ======================
# SUPPLIERS
# ======================

@api_suppliers_orders_routes.route("/api/suppliers", methods=["GET"])
def get_suppliers():
    try:
        suppliers = supplier_service.get_all_suppliers()
        return jsonify([
            {
                "supplier_id": s.supplier_id,
                "name": s.name,
                "phone": s.phone,
                "email": s.email,
                "address": s.address,
                "description": s.description,
                "created_at": s.created_at.isoformat()
            }
            for s in suppliers
        ])
    except Exception:
        return jsonify({"message": "Failed to fetch suppliers."}), 500


@api_suppliers_orders_routes.route("/api/create_supplier", methods=["POST"])
def create_supplier():
    try:
        data = request.get_json()
        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")
        description = data.get("description")

        if not name:
            return jsonify({"message": "Supplier name is required."}), 400

        supplier = supplier_service.create_supplier(name, phone, email, address, description)

        log_service.log_user_action(session.get("user_id"), f"Created supplier: {name}")
        return jsonify({"message": "Supplier added.", "supplier_id": supplier.supplier_id})
    except Exception:
        return jsonify({"message": "Failed to create supplier."}), 500


@api_suppliers_orders_routes.route("/api/update_supplier/<int:supplier_id>", methods=["PATCH"])
def update_supplier(supplier_id):
    try:
        data = request.get_json()
        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")
        description = data.get("description")

        if not name:
            return jsonify({"message": "Supplier name is required."}), 400

        success = supplier_service.update_supplier(supplier_id, name, phone, email, address, description)
        if not success:
            return jsonify({"message": "Supplier not found."}), 404

        log_service.log_user_action(session.get("user_id"), f"Updated supplier: {name} (ID: {supplier_id})")
        return jsonify({"message": "Supplier updated."})
    except Exception:
        return jsonify({"message": "Failed to update supplier."}), 500


@api_suppliers_orders_routes.route("/api/delete_supplier/<int:supplier_id>", methods=["DELETE"])
def delete_supplier(supplier_id):
    try:
        success = supplier_service.delete_supplier(supplier_id)
        if not success:
            return jsonify({"message": "Supplier not found."}), 404

        log_service.log_user_action(session.get("user_id"), f"Deleted supplier ID: {supplier_id}")
        return jsonify({"message": "Supplier deleted."})
    except Exception:
        return jsonify({"message": "Failed to delete supplier."}), 500


# ======================
# INVENTORY ORDERS
# ======================

@api_suppliers_orders_routes.route("/api/supplier_orders", methods=["GET"])
def get_orders():
    try:
        orders = inventory_order_service.get_all_orders()
        return jsonify([
            {
                "order_id": o.order_id,
                "item_name": o.item_name,
                "quantity": o.quantity,
                "status": o.status,
                "supplier_id": o.supplier_id,
                "supplier_name": o.supplier.name if o.supplier else "Unknown",
                "created_at": o.created_at.isoformat()
            }
            for o in orders
        ])
    except Exception:
        return jsonify({"message": "Failed to fetch orders."}), 500


@api_suppliers_orders_routes.route("/api/create_order", methods=["POST"])
def create_order():
    try:
        data = request.get_json()
        item_name = data.get("item_name")
        quantity = data.get("quantity")
        supplier_id = data.get("supplier_id")
        status = data.get("status", "pending")

        if not item_name or not quantity:
            return jsonify({"message": "Item name and quantity are required."}), 400

        order = inventory_order_service.create_order(item_name, quantity, supplier_id, status)

        log_service.log_user_action(session.get("user_id"), f"Created inventory order: {item_name} (Qty: {quantity})")
        return jsonify({"message": "Order placed.", "order_id": order.order_id})
    except Exception:
        return jsonify({"message": "Failed to create order."}), 500


@api_suppliers_orders_routes.route("/api/update_order/<int:order_id>", methods=["PATCH"])
def update_order(order_id):
    try:
        data = request.get_json()
        item_name = data.get("item_name")
        quantity = data.get("quantity")
        supplier_id = data.get("supplier_id")
        status = data.get("status")

        if not item_name or not quantity:
            return jsonify({"message": "Item name and quantity are required."}), 400

        success = inventory_order_service.update_order(order_id, item_name, quantity, supplier_id, status)
        if not success:
            return jsonify({"message": "Order not found."}), 404

        log_service.log_user_action(session.get("user_id"), f"Updated order ID: {order_id} ({item_name}, Qty: {quantity})")
        return jsonify({"message": "Order updated."})
    except Exception:
        return jsonify({"message": "Failed to update order."}), 500


@api_suppliers_orders_routes.route("/api/delete_order/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    try:
        success = inventory_order_service.delete_order(order_id)
        if not success:
            return jsonify({"message": "Order not found."}), 404

        log_service.log_user_action(session.get("user_id"), f"Deleted inventory order ID: {order_id}")
        return jsonify({"message": "Order deleted."})
    except Exception:
        return jsonify({"message": "Failed to delete order."}), 500
