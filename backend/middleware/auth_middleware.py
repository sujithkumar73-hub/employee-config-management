from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def jwt_required_api(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            identity = get_jwt_identity()
            request.user = identity
        except Exception as exc:
            return jsonify({"status": "error", "message": str(exc)}), 401
        return fn(*args, **kwargs)

    return wrapper
