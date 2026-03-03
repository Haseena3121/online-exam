#!/usr/bin/env python3
"""Check database schema using Flask app context"""

from app import create_app
from database import db
from sqlalchemy import inspect

def check_schema():
    app = create_app()
    
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            
            # Check if violations table exists
            tables = inspector.get_table_names()
            
            if 'violations' not in tables:
                print("❌ Violations table does NOT exist!")
                print("\n📋 Available tables:")
                for table in tables:
                    print(f"   - {table}")
                return
            
            print("✅ Violations table exists")
            
            # Get violations table columns
            columns = inspector.get_columns('violations')
            
            print(f"\n📋 Violations table columns ({len(columns)} total):")
            for col in columns:
                print(f"   {col['name']} ({col['type']})")
            
            # Check for required columns
            column_names = [col['name'] for col in columns]
            
            required_columns = ['severity', 'evidence_path', 'trust_score_reduction']
            missing = [col for col in required_columns if col not in column_names]
            
            if missing:
                print(f"\n❌ Missing columns: {', '.join(missing)}")
            else:
                print("\n✅ All required columns exist")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    check_schema()
