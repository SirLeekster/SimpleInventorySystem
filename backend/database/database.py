from backend.database import db


def create_user(user):
    db.session.add(user)  # Marks the user object to be added to the DB
    db.session.commit()  # Commit the changes to the database
