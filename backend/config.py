from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:Camottroithuongnho16@expense-tracker-db.cdsa8osuwet3.us-east-2.rds.amazonaws.com:5432/expense_tracker_user",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Camottroithuongnho16@expense-tracker-db.cdsa8osuwet3.us-east-2.rds.amazonaws.com:5432/expense_tracker_user"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
