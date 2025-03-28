import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key-default')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POLAR_CLIENT_ID = os.getenv('POLAR_CLIENT_ID')
    POLAR_CLIENT_SECRET = os.getenv('POLAR_CLIENT_SECRET')