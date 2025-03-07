from backend.models.user import User
from backend.database import database


def register(data):
    try:
        # Create a new user from the provided data
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash')
        )

        # Try to create the user in the database
        database.create_user(new_user)

        # If successful, return True
        return True
    except Exception as e:
        # Return False if an error occurs
        return False
