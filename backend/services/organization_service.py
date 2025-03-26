from backend.models.organization import Organization

def organization_exists(name: str) -> bool:
    # Check if an organization with the given name exists.
    return get_organization_by_name(name) is not None

def get_organization_by_name(name: str) -> Organization | None:
    # Return the Organization instance by name, or None if not found.
    if not name:
        return None
    return Organization.query.filter_by(organization_name=name.strip()).first()

def create_organization(name: str) -> Organization:
    #Create a new organization and return it.
    org = Organization(organization_name=name.strip())
    from backend.database import db
    db.session.add(org)
    db.session.commit()
    return org
