import os
import tempfile
from backend import create_app
from backend.database.db import db


def test_health_check_returns_success():
    os.environ["APP_MODE"] = "DEV"
    os.environ["DATABASE_URL"] = "sqlite:///./backend/instance/test.db"
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        client = app.test_client()
        response = client.get("/api/health")
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["status"] == "success"
        assert payload["app_mode"] == "Development"


def test_status_check_requires_database_access():
    os.environ["APP_MODE"] = "DEV"
    os.environ["DATABASE_URL"] = "sqlite:///./backend/instance/test.db"
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        client = app.test_client()
        response = client.get("/api/status")
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["status"] == "success"
        assert isinstance(payload["total_employees"], int)
