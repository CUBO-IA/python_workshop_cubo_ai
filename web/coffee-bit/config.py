import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "coffee-bit-dev-key")
    APP_NAME = "Coffee-bit"
    ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = ENV == "development"
