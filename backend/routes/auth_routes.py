from flask import Blueprint, request, jsonify
from backend.controllers.auth_controller import authenticate_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(force=True)
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        return jsonify({"status": "error", "message": "username and password are required"}), 400

    result = authenticate_user(username, password)
    if not result:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    return jsonify({"status": "success", "data": result}), 200
