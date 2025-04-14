from flask import Blueprint, request, jsonify, session
from backend.services import user_service, report_service

api_sales_routes = Blueprint('api_sales_routes', __name__)

# ========================
# Sales Report ROUTES
# ========================
@api_sales_routes.route("/api/sales_report", methods=['GET'])
def get_sales_report():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user = user_service.get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404

    # 🔒 Only staff and admin can view sales report
    if not user_service.user_has_role(user.user_id, ['admin', 'staff']):
        return jsonify({"message": "Access denied"}), 403

    date_range = request.args.get("range", "7d")  # default to last 7 days
    report_data = report_service.get_sales_report_for_org(user.organization_id, date_range)

    return jsonify(report_data), 200
