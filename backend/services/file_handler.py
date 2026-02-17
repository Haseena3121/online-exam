"""
File upload and storage service
"""
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    """Handle file uploads and storage"""
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm', 'pdf', 'doc', 'docx'}
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
    
    @staticmethod
    def allowed_file(filename):
        """Check if file is allowed"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FileHandler.ALLOWED_EXTENSIONS
    
    @staticmethod
    def save_evidence_file(file, folder='evidence'):
        """Save evidence file"""
        try:
            if not file or file.filename == '':
                return None
            
            if not FileHandler.allowed_file(file.filename):
                logger.warning(f"File not allowed: {file.filename}")
                return None
            
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > FileHandler.MAX_FILE_SIZE:
                logger.warning(f"File too large: {file.filename}")
                return None
            
            # Create folder if not exists
            upload_folder = os.path.join('uploads', folder)
            os.makedirs(upload_folder, exist_ok=True)
            
            # Generate secure filename
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{file_ext}"
            filepath = os.path.join(upload_folder, filename)
            
            # Save file
            file.save(filepath)
            logger.info(f"File saved: {filepath}")
            
            return f'/uploads/{folder}/{filename}'
            
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            return None
    
    @staticmethod
    def delete_file(filepath):
        """Delete file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"File deleted: {filepath}")
                return True
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
        
        return False
    
    @staticmethod
    def get_file_size(filepath):
        """Get file size"""
        try:
            return os.path.getsize(filepath)
        except Exception as e:
            logger.error(f"Error getting file size: {str(e)}")
            return 0

file_handler = FileHandler()