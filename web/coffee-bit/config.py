import os


class Config:
    ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = ENV == "development"

    SECRET_KEY = os.environ.get("SECRET_KEY")
    APP_NAME = "Coffee-bit"

    if ENV != "development":
        if not SECRET_KEY:
            raise RuntimeError(
                "SECRET_KEY debe definirse en el entorno fuera de development."
            )

    # Solo para desarrollo local; nunca usar en produccion.
    SECRET_KEY = SECRET_KEY or "coffee-bit-dev-key"
