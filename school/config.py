from dotenv import load_dotenv
import os

load_dotenv()


class Config:

    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = True

    PASSWORD_RESET_URL = os.getenv("PASSWORD_RESET_URL")


class TestConfig:

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-secret-key"
    JWT_SECRET_KEY = "test-jwt-secret-key-with-more-length-for-security-32bytes"

    MAIL_SERVER = "smtp.example.com"
    MAIL_PORT = 587
    MAIL_USERNAME = "test@example.com"
    MAIL_PASSWORD = "test-password"
    MAIL_USE_TLS = True

    PASSWORD_RESET_URL = "http://localhost:3000/reset-password"
    FRONTEND_URL = "http://localhost:5173"