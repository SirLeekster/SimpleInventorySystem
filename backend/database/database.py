from backend.database import db
from backend.models.inventory_item import Inventory_Item

def create_user(user):
    db.session.add(user)  # Marks the user object to be added to the DB
    db.session.commit()  # Commit the changes to the database

def get_inventory_items():
    return db.session.query(Inventory_Item).all()

def add_inventory_item(item):
    db.session.add(item)
    db.session.commit()