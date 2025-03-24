from backend.models.user import User
from backend.database import database


def add_user_to_db(user_data):
    try:
        new_user = User(
            username=user_data.get('username'),
            email=user_data.get('email'),
            password_hash=user_data.get('password_hash')
        )

        database.create_user(new_user)
        return True
    except Exception as e:
        print("Error in add_user_to_db:", e)
        if "Duplicate entry" in str(e):
            return "duplicate"
        return False

