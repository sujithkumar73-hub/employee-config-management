import os
from backend.database.db import db
from backend.models.user import User
from backend.models.employee import Employee


def initialize_database(app):
    database_path = app.config.get("DATABASE_URL", "sqlite:///./backend/instance/dev.db")
    local_path = database_path
    if database_path.startswith("sqlite:///"):
        local_path = database_path.replace("sqlite:///", "", 1)

    if local_path.startswith("/") and os.name == "nt":
        local_path = local_path.lstrip("/")

    if not os.path.exists(os.path.dirname(local_path)):
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

    with app.app_context():
        db.create_all()
        seed_user(app)
        if app.config.get("APP_MODE") == "Development":
            seed_sample_employees()


def seed_user(app):
    admin_username = app.config.get("ADMIN_USERNAME", "admin")
    admin_password = app.config.get("ADMIN_PASSWORD", "ChangeMe123!")
    if not User.query.filter_by(username=admin_username).first():
        user = User(username=admin_username)
        user.set_password(admin_password)
        db.session.add(user)
        db.session.commit()


def seed_sample_employees():
    if Employee.query.first():
        return

    sample_employees = [
        {"name": "Aisha Khan", "email": "aisha.khan@example.com", "department": "Human Resources", "designation": "HR Specialist", "salary": 55000},
        {"name": "Luis Castro", "email": "luis.castro@example.com", "department": "Engineering", "designation": "DevOps Engineer", "salary": 88000},
        {"name": "Maria Chen", "email": "maria.chen@example.com", "department": "Marketing", "designation": "Campaign Manager", "salary": 65000},
    ]

    for entry in sample_employees:
        employee = Employee(**entry)
        db.session.add(employee)

    db.session.commit()
