import os
from datetime import timedelta
import secrets

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'pdf'}
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Free tier limits
    FREE_MAX_FILES = 3
    FREE_MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB instead of 10MB
    FREE_TOTAL_SIZE_LIMIT = 15 * 1024 * 1024  # 15MB total (reduced proportionally)
    FREE_COMPRESSION_QUALITY = '/screen'  # Low quality for free tier
    
    # Premium tier limits
    PREMIUM_MAX_FILES = 20
    PREMIUM_MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    PREMIUM_TOTAL_SIZE_LIMIT = 500 * 1024 * 1024  # 500MB total
    PREMIUM_COMPRESSION_QUALITY = '/prepress'  # Highest quality for premium
    
    # PDF Processing Options
    PDF_QUALITY_OPTIONS = {
        'free': {
            'garbage': 4,  # Maximum garbage collection
            'deflate': True,  # Use deflate compression
            'clean': True  # Remove unused elements
        },
        'premium': {
            'garbage': 0,  # No garbage collection
            'deflate': False,  # No compression
            'clean': False,  # Preserve all elements
            'pretty': True  # Pretty print PDF structure
        }
    }
    
    # Enable CORS headers for AJAX requests
    CORS_HEADERS = 'Content-Type'

    # Celery Configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

    # Connection and timeout settings
    REQUEST_TIMEOUT = 30  # 30 seconds
    MERGE_OPERATION_TIMEOUT = 300  # 5 minutes
    MAX_RETRIES = 3

    # Server resource limits
    MAX_CONCURRENT_MERGES = 10
    RATE_LIMIT_PER_USER = '10 per minute'
    
    # Error handling settings
    RETRY_DELAYS = [1, 3, 5]  # Seconds between retries
    ERROR_LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB

    # Create upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)