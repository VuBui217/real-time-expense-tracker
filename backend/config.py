from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:610199@localhost:5433/expense_tracker_user",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:610199@localhost:5433/expense_tracker_user"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
