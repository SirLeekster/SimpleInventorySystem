import os

class Config:
    # database settings
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'root'
    DB_NAME = 'simpleinventorysystem'

    # mysql + mysqlconnector as the database dialect
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # set a secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'

    # configuration for inventory image uploads
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'frontend', 'static', 'image_uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
