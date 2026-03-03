#!/usr/bin/env python3
"""Fix database by recreating all tables"""

import os
import sys
from database import db
from config import Config

def fix_database():
    """Recreate all database tables"""
    
    # Import Flask app factory
    from app import create_app
    
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Fixing database...")
            
            # Drop all tables
            print("   Dropping all tables...")
            db.drop_all()
            
            # Create all tables
            print("   Creating all tables...")
            db.create_all()
            
            print("✅ Database fixed successfully!")
            print("\n📋 Tables created:")
            
            # List all tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            for table_name in inspector.get_table_names():
                print(f"   - {table_name}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    fix_database()
