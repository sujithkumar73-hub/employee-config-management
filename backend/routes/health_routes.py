from flask import Blueprint, jsonify, current_app
from sqlalchemy import text
from backend.database.db import db
from backend.models.employee import Employee

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    db_status = "ready"
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        db_status = "failed"

    return jsonify(
        {
            "status": "success",
            "app_mode": current_app.config.get("APP_MODE"),
            "environment": current_app.config.get("FLASK_ENV"),
            "api_url": current_app.config.get("API_URL"),
            "database": db_status,
        }
    ), 200


@health_bp.route("/status", methods=["GET"])
def status():
    employee_count = Employee.query.count()
    return jsonify(
        {
            "status": "success",
            "app_mode": current_app.config.get("APP_MODE"),
            "feature_debug": current_app.config.get("FEATURE_DEBUG"),
            "total_employees": employee_count,
        }
    ), 200


@health_bp.route("/config-check", methods=["GET"])
def config_check():
    config_values = {
        "APP_MODE": current_app.config.get("APP_MODE"),
        "FLASK_ENV": current_app.config.get("FLASK_ENV"),
        "DATABASE_URL": current_app.config.get("DATABASE_URL"),
        "API_URL": current_app.config.get("API_URL"),
        "LOG_LEVEL": current_app.config.get("LOG_LEVEL"),
        "FEATURE_DEBUG": current_app.config.get("FEATURE_DEBUG"),
    }
    return jsonify({"status": "success", "config": config_values}), 200
