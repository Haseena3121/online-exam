"""
Evidence Retention Configuration
Configure how long violation evidence is kept
"""

# Evidence retention settings
EVIDENCE_RETENTION_HOURS = 48  # Keep evidence for 2 days (48 hours)
EVIDENCE_DIR = 'uploads/evidence'

# Auto-cleanup settings
AUTO_CLEANUP_ENABLED = True  # ENABLED - Automatically delete evidence after 48 hours
AUTO_CLEANUP_INTERVAL_HOURS = 6  # Run cleanup every 6 hours

# Storage limits
MAX_EVIDENCE_SIZE_MB = 1000  # Maximum total evidence storage (1 GB)
MAX_FILE_SIZE_MB = 10  # Maximum single file size (10 MB)

# Evidence types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm'}

# Compression settings
COMPRESS_IMAGES = True  # Compress images to save space
IMAGE_QUALITY = 85  # JPEG quality (1-100)
MAX_IMAGE_DIMENSION = 1920  # Max width/height in pixels

def get_retention_hours():
    """Get evidence retention period in hours"""
    return EVIDENCE_RETENTION_HOURS

def get_retention_days():
    """Get evidence retention period in days"""
    return EVIDENCE_RETENTION_HOURS / 24

def is_auto_cleanup_enabled():
    """Check if automatic cleanup is enabled"""
    return AUTO_CLEANUP_ENABLED

def get_evidence_dir():
    """Get evidence directory path"""
    return EVIDENCE_DIR
