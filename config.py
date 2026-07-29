import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "careconnect_secret_key"

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:peace123@localhost:5432/careconnect"

    SQLALCHEMY_TRACK_MODIFICATIONS = False