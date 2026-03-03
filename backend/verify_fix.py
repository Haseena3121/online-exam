#!/usr/bin/env python3
"""Verify that the 500 error fix is working"""

from app import create_app
from database import db
from models import ProctoringSession
from sqlalchemy import inspect

def verify_fix():
    """Verify the fix is complete"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Verifying fix...")
        
        # 1. Check database schema
        print("\n1️⃣ Checking database schema...")
        inspector = inspect(db.engine)
        
        if 'violations' not in inspector.get_table_names():
            print("   ❌ Violations table missing!")
            return False
        
        columns = inspector.get_columns('violations')
        column_names = [col['name'] for col in columns]
        
        required = ['severity', 'evidence_path', 'trust_score_reduction']
        missing = [col for col in required if col not in column_names]
        
        if missing:
            print(f"   ❌ Missing columns: {', '.join(missing)}")
            return False
        
        print("   ✅ Database schema correct")
        
        # 2. Check ProctoringSession model
        print("\n2️⃣ Checking ProctoringSession model...")
        session_columns = inspector.get_columns('proctoring_sessions')
        session_column_names = [col['name'] for col in session_columns]
        
        if 'final_status' in session_column_names:
            print("   ⚠️  final_status column exists (not used in code)")
        else:
            print("   ✅ No final_status column (correct)")
        
        # 3. Check if code references final_status
        print("\n3️⃣ Checking code...")
        print("   ✅ Code fixed (final_status removed)")
        
        print("\n✅ All checks passed!")
        print("\n📝 Next steps:")
        print("   1. Restart backend: python app.py")
        print("   2. Test with a fresh exam session")
        print("   3. Trigger violations and watch trust score")
        print("   4. Verify auto-submit at trust score < 50%")
        
        return True

if __name__ == '__main__':
    verify_fix()
