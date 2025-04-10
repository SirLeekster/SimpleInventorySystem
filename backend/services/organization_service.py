from backend.models.organization import Organization
from backend.models.user import User
from backend.models.user_log import UserLog

def organization_exists(name: str) -> bool:
    # Check if an organization with the given name exists.
    return get_organization_by_name(name) is not None

def get_organization_by_name(name: str) -> Organization | None:
    # Return the Organization instance by name, or None if not found.
    if not name:
        return None
    return Organization.query.filter_by(organization_name=name.strip()).first()

def create_organization(name: str, created_by: int) -> Organization:
    org = Organization(
        organization_name=name.strip(),
        created_by=created_by
    )
    from backend.database import db
    db.session.add(org)
    db.session.commit()
    return org

def get_users_for_org(organization_id: int) -> list[User]:
    # Return a list of users that belong to the organization.
    return User.query.filter_by(organization_id=organization_id).all()

def get_all_logs_for_org(organization_id: int) -> list[UserLog]:
    # Return all logs for users that belong to the organization.
    return UserLog.query.join(User).filter(User.organization_id == organization_id).order_by(UserLog.timestamp.desc()).all()
