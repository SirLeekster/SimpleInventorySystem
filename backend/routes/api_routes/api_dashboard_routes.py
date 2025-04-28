from flask import Blueprint, jsonify, session
from backend.services import inventory_service, user_service

api_dashboard_routes = Blueprint('api_dashboard_routes', __name__)


# ========================
# DASHBOARD ROUTES
# ========================

# get dashboard statistics for the user's organization
@api_dashboard_routes.route('/api/dashboard_stats', methods=['GET'])
def get_dashboard_stats():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    org_id = user.organization_id
    stats = inventory_service.get_dashboard_stats_for_org(org_id)

    return jsonify(stats), 200
