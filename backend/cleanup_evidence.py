#!/usr/bin/env python3
"""
Cleanup old evidence files (configurable retention period)
Run this script manually or as a cron job
"""
import os
from datetime import datetime, timedelta
import logging
from config_evidence import EVIDENCE_DIR, EVIDENCE_RETENTION_HOURS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_AGE_HOURS = EVIDENCE_RETENTION_HOURS  # From config (default: 48 hours)

def cleanup_old_evidence():
    """Delete evidence files older than configured retention period"""
    try:
        if not os.path.exists(EVIDENCE_DIR):
            logger.warning(f"Evidence directory not found: {EVIDENCE_DIR}")
            return
        
        cutoff_time = datetime.now() - timedelta(hours=MAX_AGE_HOURS)
        deleted_count = 0
        total_size = 0
        
        logger.info(f"Starting cleanup of files older than {MAX_AGE_HOURS} hours...")
        logger.info(f"Cutoff time: {cutoff_time}")
        
        for filename in os.listdir(EVIDENCE_DIR):
            if filename == '.gitkeep':
                continue
            
            filepath = os.path.join(EVIDENCE_DIR, filename)
            
            # Skip if not a file
            if not os.path.isfile(filepath):
                continue
            
            # Get file modification time
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            file_size = os.path.getsize(filepath)
            
            # Delete if older than cutoff
            if file_time < cutoff_time:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                    total_size += file_size
                    logger.info(f"Deleted: {filename} (age: {datetime.now() - file_time}, size: {file_size} bytes)")
                except Exception as e:
                    logger.error(f"Failed to delete {filename}: {str(e)}")
        
        logger.info(f"Cleanup complete!")
        logger.info(f"Files deleted: {deleted_count}")
        logger.info(f"Space freed: {total_size / 1024:.2f} KB")
        
        return deleted_count, total_size
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        import traceback
        traceback.print_exc()
        return 0, 0

if __name__ == '__main__':
    print("=" * 60)
    print("🧹 EVIDENCE CLEANUP SCRIPT")
    print("=" * 60)
    print(f"Directory: {EVIDENCE_DIR}")
    print(f"Max age: {MAX_AGE_HOURS} hours")
    print("=" * 60)
    
    deleted, size = cleanup_old_evidence()
    
    print("=" * 60)
    print(f"✅ Cleanup finished!")
    print(f"   Files deleted: {deleted}")
    print(f"   Space freed: {size / 1024:.2f} KB")
    print("=" * 60)
