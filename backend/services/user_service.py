from backend.models.user import User
from backend.database import db
from backend.services import organization_service
import werkzeug.security


# add a new user to the database
def add_user_to_db(user_data):
    try:
        full_name = user_data.get('full_name')
        username = user_data.get("username")
        email = user_data.get("email")
        password = user_data.get("password")
        org_data = user_data.get("org_data", {})
        org_choice = org_data.get("org_choice")
        organization_name = org_data.get("organization_name")

        if not username or not email or not password:
            return "missing_required_fields"

        if org_choice not in ["join", "create"]:
            return "invalid_org_choice"

        if not organization_name:
            return "missing_org_name"

        if org_choice == "create":
            role = "admin"
        else:
            role = "readonly"

        # create user without org_id yet
        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
            password_hash=werkzeug.security.generate_password_hash(password),
            organization_id=None,
            role=role
        )
        db.session.add(new_user)
        db.session.flush()

        if org_choice == "create":
            org = organization_service.get_organization_by_name(organization_name)
            if org is None:
                org = organization_service.create_organization(organization_name, created_by=new_user.user_id)
        elif org_choice == "join":
            org = organization_service.get_organization_by_name(organization_name)
            if org is None:
                return "organization_not_found"

        new_user.organization_id = org.organization_id
        db.session.commit()
        return new_user

    except Exception as e:
        db.session.rollback()
        if "Duplicate entry" in str(e):
            return "duplicate"
        return "internal_error"


# log in a user by verifying credentials
def login_user(login_data):
    try:
        email = login_data.get("email")
        password = login_data.get("password")
        if not email or not password:
            return False

        user = db.session.query(User).filter_by(email=email).first()

        # using werkzeug's check_password_hash for proper password verification
        if user and werkzeug.security.check_password_hash(user.password_hash, password):
            return user
        return False
    except Exception as e:
        print(f"Login error: {e}")
        return False


# get a user by id
def get_user_by_id(user_id):
    return User.query.get(user_id)


# get a user by email
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


# check if a user has one of the required roles
def user_has_role(user_id, required_roles):
    user = get_user_by_id(user_id)
    if not user:
        return False
    return user.role in required_roles


# promote a user to a new role
def promote_user(user_id, new_role, admin_user):
    if new_role not in ['admin', 'staff', 'readonly']:
        return "invalid_role"

    target_user = get_user_by_id(user_id)
    if not target_user:
        return "not_found"

    if target_user.organization_id != admin_user.organization_id:
        return "cross_org"

    old_role = target_user.role
    target_user.role = new_role
    db.session.commit()

    return {"status": "success", "old_role": old_role, "new_role": new_role, "target_user": target_user}


# delete a user
def delete_user(user_id, admin_user):
    target_user = get_user_by_id(user_id)
    if not target_user:
        return "not_found"

    if target_user.organization_id != admin_user.organization_id:
        return "cross_org"

    if target_user.user_id == admin_user.user_id:
        return "self_delete"

    db.session.delete(target_user)
    db.session.commit()

    return {"status": "success", "target_user": target_user}
