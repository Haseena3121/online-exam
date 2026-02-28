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
    # DATABASE CONFIG (Using SQLite for easy setup)
    # ===============================
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam_proctoring.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ===============================
    # JWT CONFIG
    # ===============================
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

    # ===============================
    # ENABLE CORS (VERY IMPORTANT)
    # ===============================
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "supports_credentials": True,
            "expose_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Add OPTIONS handler for all routes
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # ===============================
    # INIT EXTENSIONS
    # ===============================
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)

    # ===============================
    # JWT ERROR HANDLERS
    # ===============================
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"Invalid token error: {error}")
        return jsonify({"error": "Invalid token", "message": str(error)}), 422

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        print(f"Unauthorized error: {error}")
        return jsonify({"error": "Missing authorization header", "message": str(error)}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print(f"Expired token")
        return jsonify({"error": "Token has expired"}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        print(f"Revoked token")
        return jsonify({"error": "Token has been revoked"}), 401

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


if __name__ == '__main__':
    app = create_app()
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified")
    
    print("=" * 60)
    print("🚀 BACKEND SERVER STARTING")
    print("=" * 60)
    print("📍 URL: http://127.0.0.1:5000")
    print("📍 Frontend should connect to: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
