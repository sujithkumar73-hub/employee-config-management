import logging
from flask import request


def register_request_logging(app):
    handler = logging.StreamHandler()
    handler.setLevel(app.config.get("LOG_LEVEL", "INFO"))
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    app.logger.handlers = [handler]
    app.logger.setLevel(app.config.get("LOG_LEVEL", "INFO"))

    @app.before_request
    def log_request():
        app.logger.debug(
            "REQUEST %s %s headers=%s body=%s",
            request.method,
            request.path,
            dict(request.headers),
            request.get_json(silent=True),
        )
