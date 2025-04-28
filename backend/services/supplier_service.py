from backend.models.supplier import Supplier
from backend.database import db


# get all suppliers ordered by creation date
def get_all_suppliers() -> list[Supplier]:
    return Supplier.query.order_by(Supplier.created_at.desc()).all()


# get a supplier by id
def get_supplier_by_id(supplier_id: int) -> Supplier | None:
    return Supplier.query.get(supplier_id)


# create a new supplier
def create_supplier(name: str, phone: str = None, email: str = None, address: str = None,
                    description: str = None) -> Supplier:
    supplier = Supplier(
        name=name.strip(),
        phone=phone.strip() if phone else None,
        email=email.strip() if email else None,
        address=address.strip() if address else None,
        description=description.strip() if description else None
    )
    db.session.add(supplier)
    db.session.commit()
    return supplier


# update an existing supplier
def update_supplier(supplier_id: int, name: str, phone: str = None, email: str = None, address: str = None,
                    description: str = None) -> bool:
    supplier = get_supplier_by_id(supplier_id)
    if not supplier:
        return False

    supplier.name = name.strip()
    supplier.phone = phone.strip() if phone else None
    supplier.email = email.strip() if email else None
    supplier.address = address.strip() if address else None
    supplier.description = description.strip() if description else None

    db.session.commit()
    return True


# delete a supplier
def delete_supplier(supplier_id: int) -> bool:
    supplier = get_supplier_by_id(supplier_id)
    if not supplier:
        return False
    db.session.delete(supplier)
    db.session.commit()
    return True
