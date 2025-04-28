from backend.models.organization import Organization
from backend.models.user import User
from backend.models.user_log import UserLog


# check if an organization exists by name
def organization_exists(name: str) -> bool:
    return get_organization_by_name(name) is not None


# get organization by name
def get_organization_by_name(name: str) -> Organization | None:
    if not name:
        return None
    return Organization.query.filter_by(organization_name=name.strip()).first()


# create a new organization
def create_organization(name: str, created_by: int) -> Organization:
    org = Organization(
        organization_name=name.strip(),
        created_by=created_by
    )
    from backend.database import db
    db.session.add(org)
    db.session.commit()
    return org


# get all users for an organization
def get_users_for_org(organization_id: int) -> list[User]:
    return User.query.filter_by(organization_id=organization_id).all()


# get all logs for an organization
def get_all_logs_for_org(organization_id: int) -> list[UserLog]:
    return UserLog.query.join(User).filter(User.organization_id == organization_id).order_by(
        UserLog.timestamp.desc()).all()
