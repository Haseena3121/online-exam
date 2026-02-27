"""
Fix database schema - add missing columns
"""
from app import create_app
from database import db
import sqlite3
import os

def fix_database():
    """Add missing columns to existing tables"""
    app = create_app()
    
    with app.app_context():
        # Get database path - handle both relative and absolute paths
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        db_path = db_uri.replace('sqlite:///', '')
        
        # If relative path, check both current dir and instance folder
        if not os.path.isabs(db_path):
            # Try instance folder first (Flask default)
            instance_path = os.path.join('instance', db_path)
            if os.path.exists(instance_path):
                db_path = instance_path
        
        print(f"📊 Fixing database: {db_path}")
        
        if not os.path.exists(db_path):
            print(f"❌ Database file not found: {db_path}")
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check and add end_time to proctoring_sessions
        try:
            cursor.execute("PRAGMA table_info(proctoring_sessions)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'end_time' not in columns:
                print("Adding end_time column to proctoring_sessions...")
                cursor.execute("ALTER TABLE proctoring_sessions ADD COLUMN end_time DATETIME")
                conn.commit()
                print("✅ Added end_time column")
            else:
                print("✅ end_time column already exists")
        except Exception as e:
            print(f"⚠️  Could not add end_time: {e}")
        
        conn.close()
        print("\n✅ Database fix complete!")

if __name__ == '__main__':
    fix_database()
