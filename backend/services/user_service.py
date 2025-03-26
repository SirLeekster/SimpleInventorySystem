from backend.models.user import User
from backend.database import db
from backend.services import organization_service

def add_user_to_db(user_data):
    try:
        full_name = user_data.get("full_name")
        email = user_data.get("email")
        password = user_data.get("password")
        org_data = user_data.get("org_data", {})
        org_choice = org_data.get("org_choice")
        organization_name = org_data.get("organization_name")

        if not full_name or not email or not password:
            return "missing_required_fields"

        if org_choice not in ["join", "create"]:
            return "invalid_org_choice"

        if not organization_name:
            return "missing_org_name"

        if org_choice == "create":
            org = organization_service.get_organization_by_name(organization_name)
            if org is None:
                org = organization_service.create_organization(organization_name)
        elif org_choice == "join":
            org = organization_service.get_organization_by_name(organization_name)
            if org is None:
                return "organization_not_found"

        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=password,
            organization_id=org.organization_id
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    except Exception as e:
        if "Duplicate entry" in str(e):
            return "duplicate"
        return "internal_error"

def login_user(login_data):
    try:
        email = login_data.get("email")
        password = login_data.get("password")
        if not email or not password:
            return False

        user = db.session.query(User).filter_by(email=email).first()
        if user and user.password_hash == password:
            return user
        return False
    except Exception:
        return False

def get_user_by_id(user_id):
    return User.query.get(user_id)