from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend.config import get_config
from backend.database.db import db
from backend.routes.auth_routes import auth_bp
from backend.routes.employee_routes import employee_bp
from backend.routes.health_routes import health_bp
from backend.middleware.logging_middleware import register_request_logging
from backend.services.seed_service import initialize_database


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config_class = get_config()
    app.config.from_object(config_class)
    config_class.init_app(app)

    CORS(app)
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(employee_bp, url_prefix="/api/employees")
    app.register_blueprint(health_bp, url_prefix="/api")
    
    @app.route("/")
    def index():
        from flask import jsonify
        return jsonify(
            {
                "status": "success",
                "message": "Employee Management System Backend API",
                "version": "1.0.0",
                "endpoints": {
                    "health": "/api/health",
                    "status": "/api/status",
                    "config": "/api/config-check",
                    "auth": "/api/auth/login",
                    "employees": "/api/employees/",
                },
                "frontend_note": "Frontend is served separately. Open frontend/index.html in your browser or use Docker Compose.",
            }
        ), 200

    register_request_logging(app)

    @app.before_request
    def setup_database():
        if not getattr(app, "db_initialized", False):
            initialize_database(app)
            app.db_initialized = True

    @app.errorhandler(400)
    def bad_request(error):
        return {"status": "error", "message": str(error)}, 400

    @app.errorhandler(401)
    def unauthorized(error):
        return {"status": "error", "message": "Unauthorized access"}, 401

    @app.errorhandler(404)
    def not_found(error):
        return {"status": "error", "message": "Resource not found"}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {"status": "error", "message": "Internal server error"}, 500

    return app
