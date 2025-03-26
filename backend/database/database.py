from backend.database import db
from backend.models.user import User
from backend.models.inventory_item import Inventory_Item

# Add the user object to the database and commit the changes
def create_user(user):
    # Mark the user object to be added to the DB
    db.session.add(user)
    # Commit the changes to save the user
    db.session.commit()

# Return the User object corresponding to the given email, or None if not found
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

# Return all inventory items from the database
def get_inventory_items():
    return Inventory_Item.query.all()

# Add an inventory item to the database and commit the changes
def add_inventory_item(item):
    db.session.add(item)
    db.session.commit()
