import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()  # Load local development env vars if present

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

API_URL = os.getenv("API_URL", "http://localhost:5000")


def normalize_sqlite_url(database_url: str) -> str:
    if not database_url.startswith("sqlite:///"):
        return database_url

    sqlite_path = database_url[10:]
    sqlite_path = sqlite_path.replace("\\", "/")
    if not os.path.isabs(sqlite_path):
        sqlite_path = os.path.abspath(os.path.join(BASE_DIR, sqlite_path)).replace("\\", "/")
    return f"sqlite:///{sqlite_path}"


class Config:
    APP_MODE = os.getenv("APP_MODE", "Development")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-env")
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_URL = normalize_sqlite_url(
        os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'dev.db')}"),
    )
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    FEATURE_DEBUG = os.getenv("FEATURE_DEBUG", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    API_URL = API_URL
    PORT = int(os.getenv("PORT", 5000))
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "ChangeMe123!")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    FEATURE_DEBUG = os.getenv("FEATURE_DEBUG", "true").lower() == "true"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    APP_MODE = "Development"
    FLASK_ENV = "development"
    DEBUG = True
    FEATURE_DEBUG = True
    LOG_LEVEL = "DEBUG"


class QAConfig(Config):
    APP_MODE = "QA"
    FLASK_ENV = "development"
    DEBUG = False
    FEATURE_DEBUG = True
    LOG_LEVEL = "DEBUG"


class UATConfig(Config):
    APP_MODE = "UAT"
    FLASK_ENV = "production"
    DEBUG = False
    FEATURE_DEBUG = False
    LOG_LEVEL = "INFO"


class ProductionConfig(Config):
    APP_MODE = "Production"
    FLASK_ENV = "production"
    DEBUG = False
    FEATURE_DEBUG = False
    LOG_LEVEL = "WARNING"


config_map = {
    "DEV": DevelopmentConfig,
    "QA": QAConfig,
    "UAT": UATConfig,
    "PROD": ProductionConfig,
}


def get_config(environment_key: str = None):
    key = environment_key or os.getenv("APP_ENV", os.getenv("APP_MODE", "DEV")).upper()
    return config_map.get(key, DevelopmentConfig)
