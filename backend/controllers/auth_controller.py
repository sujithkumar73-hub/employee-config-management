from flask import current_app
from flask_jwt_extended import create_access_token
from backend.models.user import User
from backend.database.db import db


def authenticate_user(username: str, password: str):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.username)
        return {
            "access_token": access_token,
            "user": user.to_dict(),
            "app_mode": current_app.config.get("APP_MODE"),
        }
    return None


def seed_admin_user(default_username: str, default_password: str):
    existing = User.query.filter_by(username=default_username).first()
    if existing:
        return existing

    new_user = User(username=default_username, role="admin")
    new_user.set_password(default_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user
