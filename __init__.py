"""
MiroOrca Flask Application Factory
"""

import os
from flask import Flask
from flask_cors import CORS
from .config import config
from .utils.logger import setup_logger

logger = setup_logger(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # Enable CORS for frontend dev server
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

    # Ensure required directories exist
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(config.SIMULATION_DATA_DIR, exist_ok=True)
    os.makedirs(config.LOGS_DIR, exist_ok=True)

    # Register API blueprints
    from .api import graph_bp, simulation_bp, report_bp
    app.register_blueprint(graph_bp, url_prefix="/api/graph")
    app.register_blueprint(simulation_bp, url_prefix="/api/simulation")
    app.register_blueprint(report_bp, url_prefix="/api/report")

    @app.route("/api/health")
    def health():
        return {"status": "ok", "version": "0.1.0"}

    logger.info("MiroOrca backend started")
    return app
