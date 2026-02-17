"""
Flask application factory
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta, datetime
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

from database import db, migrate
from models import *
from services.email_service import mail

load_dotenv()


def create_app():
    """Create and configure Flask application"""

    app = Flask(__name__)

    # =============================
    # DATABASE CONFIGURATION
    # =============================
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://root:1234@localhost/online_exam_proctoring'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False

    # =============================
    # JWT CONFIGURATION
    # =============================
    app.config['JWT_SECRET_KEY'] = 'change-this-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

    # =============================
    # ENABLE CORS (IMPORTANT FIX)
    # =============================
    CORS(app)   # ✅ Allow all origins (for development)

    # =============================
    # INITIALIZE EXTENSIONS
    # =============================
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    JWTManager(app)

    # =============================
    # ROOT ROUTE
    # =============================
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({
            "message": "Online Exam Proctoring Backend Running Successfully 🚀"
        }), 200

    # =============================
    # HEALTH ROUTE
    # =============================
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'app': 'Online Exam Proctoring System'
        }), 200

    # =============================
    # STATUS ROUTE
    # =============================
    @app.route('/api/status', methods=['GET'])
    def status():
        return jsonify({
            'status': 'running',
            'version': '1.0.0'
        }), 200

    return app


# =============================
# OPTIONAL LOGGING SETUP
# =============================
def setup_logging(app):
    if not app.debug:
        os.makedirs('logs', exist_ok=True)

        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,
            backupCount=10
        )

        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
        )

        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)


# =============================
# ERROR HANDLER
# =============================
def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
