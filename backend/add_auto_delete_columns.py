#!/usr/bin/env python3
"""
Add auto-deletion columns to exams table
"""

from app import create_app
from database import db

app = create_app()

with app.app_context():
    print("=== ADDING AUTO-DELETION COLUMNS ===")
    
    try:
        # Add columns using raw SQL
        with db.engine.connect() as conn:
            conn.execute(db.text("""
                ALTER TABLE exams 
                ADD COLUMN auto_delete_enabled BOOLEAN DEFAULT 0
            """))
            conn.commit()
        print("✅ Added auto_delete_enabled column")
    except Exception as e:
        print(f"⚠️  auto_delete_enabled column might already exist: {e}")
    
    try:
        with db.engine.connect() as conn:
            conn.execute(db.text("""
                ALTER TABLE exams 
                ADD COLUMN auto_delete_date DATETIME NULL
            """))
            conn.commit()
        print("✅ Added auto_delete_date column")
    except Exception as e:
        print(f"⚠️  auto_delete_date column might already exist: {e}")
    
    print("\n✅ Migration complete!")
    print("Examiners can now set auto-deletion for exams")
