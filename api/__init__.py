"""
api/__init__.py

API Package Initialization
"""

from flask import Flask
from flask_cors import CORS


def create_app() -> Flask:
    """
    Create and configure Flask application.
    """

    app = Flask(__name__)

    # Enable Cross-Origin Resource Sharing
    CORS(app)

    app.config["JSON_SORT_KEYS"] = False

    return app


__all__ = [
    "create_app"
]