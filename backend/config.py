"""
Application configuration settings
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    DEBUG = False
    TESTING = False
    
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost/online_exam_proctoring'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 500 * 1024 * 1024))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm'}
    
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@examproctoring.com')
    
    VIOLATION_TRUST_SCORE_REDUCTION = int(os.getenv('VIOLATION_TRUST_SCORE_REDUCTION', 10))
    CRITICAL_TRUST_SCORE_THRESHOLD = int(os.getenv('CRITICAL_TRUST_SCORE_THRESHOLD', 50))
    ENABLE_BLUR_BACKGROUND = os.getenv('ENABLE_BLUR_BACKGROUND', 'True').lower() == 'true'
    ENABLE_SOUND_DETECTION = os.getenv('ENABLE_SOUND_DETECTION', 'True').lower() == 'true'
    ENABLE_FACE_DETECTION = os.getenv('ENABLE_FACE_DETECTION', 'True').lower() == 'true'
    ENABLE_PHONE_DETECTION = os.getenv('ENABLE_PHONE_DETECTION', 'True').lower() == 'true'
    ENABLE_TAB_MONITORING = os.getenv('ENABLE_TAB_MONITORING', 'True').lower() == 'true'
    ENABLE_EYE_GAZE_TRACKING = os.getenv('ENABLE_EYE_GAZE_TRACKING', 'True').lower() == 'true'
    
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test-secret-key'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}