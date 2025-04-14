from flask import Blueprint, request, jsonify, session
from backend.services import user_service, organization_service, log_service
from backend.database import db
from backend.models.organization import Organization
import werkzeug.security
import traceback

api_settings_routes = Blueprint('api_settings_routes', __name__)

# ========================
# Settings ROUTES
# ========================

@api_settings_routes.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404

    organization_name = "Unknown"
    if user.organization_id:
        org = Organization.query.get(user.organization_id)
        if org:
            organization_name = org.organization_name

    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "organization_id": user.organization_id,
        "organization_name": organization_name,
        "role": user.role
    }), 200


@api_settings_routes.route('/api/user/profile', methods=['PATCH'])
def update_user_profile():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Read-only users should not be able to update anything
    if not user_service.user_has_role(user.user_id, ['admin', 'staff']):
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    if 'email' in data and data['email'] != user.email:
        existing_user = user_service.get_user_by_email(data['email'])
        if existing_user and existing_user.user_id != user.user_id:
            return jsonify({"message": "Email already in use"}), 409
        user.email = data['email']

    if 'username' in data:
        user.username = data['username']

    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({"message": f"Failed to update profile: {str(e)}"}), 500


@api_settings_routes.route('/api/user/password', methods=['POST'])
def change_user_password():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    if not data or 'current_password' not in data or 'new_password' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    if not werkzeug.security.check_password_hash(user.password_hash, data['current_password']):
        return jsonify({"message": "Current password is incorrect"}), 401

    user.password_hash = werkzeug.security.generate_password_hash(data['new_password'])

    try:
        db.session.commit()
        return jsonify({"message": "Password changed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to change password: {str(e)}"}), 500


@api_settings_routes.route('/api/org/users', methods=['GET'])
def get_users_for_organization():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user = user_service.get_user_by_id(session['user_id'])
    if not user or not user_service.user_has_role(user.user_id, ['admin', 'staff']):
        return jsonify({"message": "Access denied"}), 403

    users = organization_service.get_users_for_org(user.organization_id)
    result = [{
        "user_id": u.user_id,
        "username": u.username,
        "email": u.email,
        "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "role": u.role
    } for u in users]

    return jsonify({"users": result}), 200


@api_settings_routes.route('/api/org/logs', methods=['GET'])
def get_all_logs_for_organization():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user = user_service.get_user_by_id(session['user_id'])
    if not user or not user_service.user_has_role(user.user_id, ['admin','staff']):
        return jsonify({"message": "Access denied"}), 403

    logs = log_service.get_all_logs_for_org(user.organization_id)
    return jsonify({"logs": logs}), 200

@api_settings_routes.route('/api/promote_user', methods=['PATCH'])
def promote_user_route():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    admin = user_service.get_user_by_id(session['user_id'])
    if not admin or not user_service.user_has_role(admin.user_id, ['admin']):
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()
    user_id = data.get("user_id")
    new_role = data.get("role")

    result = user_service.promote_user(user_id, new_role, admin)

    if isinstance(result, dict) and result.get("status") == "success":
        from backend.services import log_service
        log_service.log_user_action(
            admin.user_id,
            f"Changed role for user ID {result['target_user'].user_id} from '{result['old_role']}' to '{result['new_role']}'"
        )
        return jsonify({"message": f"User promoted to {result['new_role']}"}), 200

    if result == "not_found":
        return jsonify({"message": "User not found"}), 404
    if result == "cross_org":
        return jsonify({"message": "Cross-org access denied"}), 403
    if result == "invalid_role":
        return jsonify({"message": "Invalid role"}), 400
    return jsonify({"message": "Promotion failed"}), 500

@api_settings_routes.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    admin = user_service.get_user_by_id(session['user_id'])
    if not admin or not user_service.user_has_role(admin.user_id, ['admin']):
        return jsonify({"message": "Access denied"}), 403

    result = user_service.delete_user(user_id, admin)

    if isinstance(result, dict) and result.get("status") == "success":
        from backend.services import log_service
        log_service.log_user_action(
            admin.user_id,
            f"Deleted user ID {result['target_user'].user_id} - {result['target_user'].username}"
        )
        return jsonify({"message": "User deleted successfully"}), 200

    if result == "not_found":
        return jsonify({"message": "User not found"}), 404
    if result == "cross_org":
        return jsonify({"message": "Cannot delete users from another organization"}), 403
    if result == "self_delete":
        return jsonify({"message": "You cannot delete your own account"}), 400
    return jsonify({"message": "User deletion failed"}), 500

# ========================
# Debug / Testing Routes
# ========================

@api_settings_routes.route('/api/test-session', methods=['GET'])
def test_session():
    if 'user_id' in session:
        return jsonify({"message": f"Session active with user_id: {session['user_id']}"}), 200
    return jsonify({"message": "No user in session"}), 401


@api_settings_routes.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({"message": "API is working"}), 200


@api_settings_routes.route('/api/user/test', methods=['GET'])
def test_user_api():
    if 'user_id' in session:
        return jsonify({"message": f"Found user_id in session: {session['user_id']}"}), 200
    return jsonify({"message": "No user_id in session"}), 401


@api_settings_routes.route('/api/user/profile-simple', methods=['GET'])
def get_user_profile_simple():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401
    return jsonify({
        "username": "Test User",
        "email": "test@example.com",
        "organization_name": "Test Organization"
    }), 200


@api_settings_routes.route('/api/reset-admin-password', methods=['GET'])
def reset_admin_password():
    try:
        user = user_service.get_user_by_id(1)
        if not user:
            return jsonify({"message": "Admin user not found"}), 404

        new_password = "admin123"
        user.password_hash = werkzeug.security.generate_password_hash(new_password)
        db.session.commit()
        return jsonify({"message": "Admin password reset", "new_password": new_password}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500


@api_settings_routes.route('/api/logs/recent', methods=['GET'])
def get_recent_logs():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404

    logs = log_service.get_recent_logs_for_org(user.organization_id)
    return jsonify({'logs': logs}), 200
