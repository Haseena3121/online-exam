"""
Check DB tables exist and recreate if missing.
Run: python check_and_fix_db.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from database import db

app = create_app()

with app.app_context():
    try:
        db.create_all()
        print("✅ All tables verified/created.")

        # Test insert a dummy query
        from models import User
        count = User.query.count()
        print(f"✅ Users table OK — {count} users currently.")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
