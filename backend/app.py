from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import load_dotenv

from database import db, migrate
from routes.auth import auth_bp
from routes.exam import exam_bp
from routes.results import results_bp
from routes.examiner import examiner_bp
from routes.proctoring import proctoring_bp
from routes.violations import violations_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    # ===============================
    # DATABASE CONFIG
    # ===============================
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://root:1234@localhost/online_exam_proctoring'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ===============================
    # JWT CONFIG
    # ===============================
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

    # ===============================
    # ENABLE CORS (VERY IMPORTANT)
    # ===============================
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # ===============================
    # INIT EXTENSIONS
    # ===============================
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    # ===============================
    # REGISTER ALL BLUEPRINTS
    # ===============================
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(exam_bp, url_prefix="/api/exams")
    app.register_blueprint(results_bp, url_prefix="/api/results")
    app.register_blueprint(examiner_bp, url_prefix="/api/examiner")
    app.register_blueprint(proctoring_bp, url_prefix="/api/proctoring")
    app.register_blueprint(violations_bp, url_prefix="/api/violations")

    # ===============================
    # TEST ROUTE
    # ===============================
    @app.route("/")
    def home():
        return jsonify({"message": "Backend Running Successfully 🚀"})

    return app