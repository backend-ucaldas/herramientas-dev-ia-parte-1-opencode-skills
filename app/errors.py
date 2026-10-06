from flask import jsonify


class ApiError(Exception):
    status_code = 400

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ValidationError(ApiError):
    status_code = 400


class NotFoundError(ApiError):
    status_code = 404


class ConflictError(ApiError):
    status_code = 409


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(404)
    def handle_not_found(_error):
        return jsonify({"error": "Route not found"}), 404

    @app.errorhandler(500)
    def handle_unexpected_error(_error):
        return jsonify({"error": "Internal server error"}), 500
