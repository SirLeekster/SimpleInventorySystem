from flask import Blueprint, request, jsonify, session
from backend.services import user_service, inventory_service
from backend.models.user import User
from backend.models.inventory_item import Inventory_Item 
from backend.database import db 

api_routes = Blueprint('api_routes', __name__)

# ========================
# USER ROUTES
# ========================

@api_routes.route('/api/create_user', methods=['POST'])
def create_user():
    user_data = request.get_json()
    print("Received user data:", user_data)
    if not user_data:
        return jsonify({"message": "No JSON received"}), 400

    new_user = user_service.add_user_to_db(user_data)
    if new_user and isinstance(new_user, User):
        return jsonify({"message": "User created successfully"}), 201
    elif new_user == "duplicate":
        return jsonify({"message": "Email already exists"}), 409
    elif new_user == "organization_not_found":
        return jsonify({"message": "Organization not found"}), 404
    else:
        return jsonify({"message": "Failed to create user"}), 400

@api_routes.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = user_service.login_user(data)
    if user:
        session['user_id'] = user.user_id
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

# ========================
# INVENTORY ROUTES
# ========================


@api_routes.route('/api/upc_lookup', methods=['GET'])
def upc_lookup():
    upc = request.args.get('upc')
    if not upc:
        return jsonify({"message": "UPC is required"}), 400

    try:
        import requests
        response = requests.get(f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}")
        data = response.json()

        if response.status_code != 200 or not data.get("items"):
            return jsonify({"message": "No data found for that UPC"}), 404

        item = data["items"][0]
        return jsonify({
            "product_name": item.get("title", ""),
            "description": item.get("description", ""),
            "category": item.get("category", ""),
            "price": item.get("lowest_recorded_price", "")
        }), 200


    except Exception as e:
        return jsonify({"message": f"Error during UPC lookup: {str(e)}"}), 500



@api_routes.route('/api/create_inventory_item', methods=['POST'])
def create_inventory_item():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    item_data = request.get_json()
    if not item_data:
        return jsonify({"message": "Invalid or missing JSON"}), 400

    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404

    result = inventory_service.add_inventory_item_to_db(item_data, user)
    if result and isinstance(result, Inventory_Item):
        return jsonify({
            "message": "Inventory item created successfully",
            "item_id": result.id  # <-- required!
        }), 201
    print("Inventory creation failed with data:", item_data)
    return jsonify({"message": "Failed to create inventory item"}), 400



@api_routes.route('/api/upload_inventory_image/<int:item_id>', methods=['POST'])
def upload_inventory_image(item_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    if 'image' not in request.files:
        return jsonify({"message": "No image provided"}), 400

    image = request.files['image']

    from backend.services.inventory_service import save_inventory_image
    success, result = save_inventory_image(item_id, image)
    print(f"Image upload result: {result} + {item_id}")

    if success:
        return jsonify({"message": "Image uploaded successfully", "image_path": result}), 200
    else:
        return jsonify({"message": result}), 400



@api_routes.route('/api/update_inventory_quantity/<int:item_id>', methods=['PUT'])
def update_inventory_quantity(item_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    data = request.get_json()
    if not data or 'change' not in data:
        return jsonify({"message": "Missing 'change' in request body"}), 400

    change = data['change']

    try:
        updated_item = inventory_service.update_item_quantity(item_id, change)
        return jsonify({
            "message": "Item quantity updated successfully",
            "item_id": updated_item.item_id,
            "new_quantity": updated_item.quantity
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api_routes.route('/api/inventory_items', methods=['GET'])
def get_inventory_items():
    print("🔍 Route /api/inventory_items was hit!")

    if 'user_id' not in session:
        print("❌ No user in session")
        return jsonify({"message": "Not authenticated"}), 401

    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        print("❌ User not found")
        return jsonify({"message": "User not found"}), 404

    items = inventory_service.get_items_for_org(user.organization_id)

    print(f"✅ Found {len(items)} inventory items")

    data = [
        {
            "id": item.id,
            "product_name": item.product_name,
            "description": item.description,
            "category": item.category,
            "quantity": item.quantity,
            "price": str(item.price),
            "image_path": item.image_path or ""
        }
        for item in items
    ]

    return jsonify(data), 200

@api_routes.route('/api/update_inventory_item/<int:item_id>', methods=['PATCH'])
def update_inventory_item(item_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid or missing JSON"}), 400

    # Fetch the item to be updated
    item = Inventory_Item.query.get(item_id)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    # Update item fields from the data
    item.product_name = data.get("product_name", item.product_name)
    item.description = data.get("description", item.description)
    item.category = data.get("category", item.category)
    item.quantity = data.get("quantity", item.quantity)
    item.price = data.get("price", item.price)

    try:
        db.session.commit()
        return jsonify({"message": "Item updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to update item: {str(e)}"}), 500

@api_routes.route('/api/delete_inventory_item/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    # Fetch the item to delete
    item = Inventory_Item.query.get(item_id)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to delete item: {str(e)}"}), 500


# ========================
# DASHBOARD ROUTES
# ========================
@api_routes.route('/api/dashboard_stats', methods=['GET'])
def get_dashboard_stats():
    from backend.services import inventory_service, user_service

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    org_id = user.organization_id
    stats = inventory_service.get_dashboard_stats_for_org(org_id)

    return jsonify(stats), 200


# ========================
# Settings ROUTES
# ========================

@api_routes.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    
    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Get organization name - this is the part that needs fixing
    organization_name = "Unknown"
    if user.organization_id:
        from backend.models.organization import Organization
        org = Organization.query.get(user.organization_id)
        if org:
            # Make sure this matches your database column name
            organization_name = org.organization_name  # Use organization_name not name
    
    # Return user profile data
    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "organization_id": user.organization_id,
        "organization_name": organization_name
    }), 200

@api_routes.route('/api/user/profile', methods=['PATCH'])
def update_user_profile():
    try:
        if 'user_id' not in session:
            return jsonify({"message": "Not authenticated"}), 401
        
        user = user_service.get_user_by_id(session['user_id'])
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        # Print debug information
        print(f"Update profile request for user ID: {session['user_id']}")
        print(f"Request data: {data}")
        
        # Check if email is being changed and if it's already in use
        if 'email' in data and data['email'] != user.email:
            existing_user = user_service.get_user_by_email(data['email'])
            if existing_user and existing_user.user_id != user.user_id:
                return jsonify({"message": "Email already in use"}), 409
            user.email = data['email']
        
        # Update username
        if 'username' in data:
            user.username = data['username']
        
        print("About to commit changes to database")
        db.session.commit()
        print("Changes committed successfully")
        
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()  # Print detailed stack trace
        print(f"Error updating profile: {str(e)}")
        return jsonify({"message": f"Failed to update profile: {str(e)}"}), 500
        
@api_routes.route('/api/user/password', methods=['POST'])
def change_user_password():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    
    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.get_json()
    if not data or 'current_password' not in data or 'new_password' not in data:
        return jsonify({"message": "Missing required fields"}), 400
    
    current_password = data['current_password']
    new_password = data['new_password']
    
    # Verify current password
    import werkzeug.security
    if not werkzeug.security.check_password_hash(user.password_hash, current_password):
        return jsonify({"message": "Current password is incorrect"}), 401
    
    # Update password
    user.password_hash = werkzeug.security.generate_password_hash(new_password)
    
    try:
        db.session.commit()
        return jsonify({"message": "Password changed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to change password: {str(e)}"}), 500
    


@api_routes.route('/api/test-session', methods=['GET'])
def test_session():
    if 'user_id' in session:
        return jsonify({"message": f"Session active with user_id: {session['user_id']}"}), 200
    else:
        return jsonify({"message": "No user in session"}), 401
    

@api_routes.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({"message": "API is working"}), 200

@api_routes.route('/api/user/test', methods=['GET'])
def test_user_api():
    if 'user_id' in session:
        user_id = session['user_id']
        return jsonify({"message": f"Found user_id in session: {user_id}"}), 200
    else:
        return jsonify({"message": "No user_id in session"}), 401
    
@api_routes.route('/api/user/profile-simple', methods=['GET'])
def get_user_profile_simple():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    
    # Return hardcoded test data instead of database query
    return jsonify({
        "username": "Test User",
        "email": "test@example.com",
        "organization_name": "Test Organization"
    }), 200

@api_routes.route('/api/reset-admin-password', methods=['GET'])
def reset_admin_password():
    # Only use this temporarily for fixing the admin password
    try:
        user = user_service.get_user_by_id(1)  # Assuming admin has user_id 1
        if not user:
            return jsonify({"message": "Admin user not found"}), 404
        
        # Set a new known password with proper hashing
        import werkzeug.security
        new_password = "admin123"  # Choose your new password
        user.password_hash = werkzeug.security.generate_password_hash(new_password)
        
        db.session.commit()
        
        return jsonify({
            "message": "Admin password has been reset",
            "new_password": new_password
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500