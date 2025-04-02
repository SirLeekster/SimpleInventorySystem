import os

class Config:
    # Database settings
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'root'
    DB_NAME = 'simpleinventorysystem'

    # Use mysql+mysqlconnector as the database dialect
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy track modifications

    # Set a secret key (in a real project, use a secure, random value and keep it secret)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'

    # configuration for inventory image uploads
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'frontend', 'static', 'image_uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
