#!/usr/bin/env python3
"""
Reset examiner password to a known value
"""

from app import create_app
from database import db
from models import User

app = create_app()

with app.app_context():
    print("=== RESETTING EXAMINER PASSWORDS ===")
    
    examiners = User.query.filter_by(role='examiner').all()
    
    for examiner in examiners:
        print(f"\nExaminer: {examiner.name} ({examiner.email})")
        
        # Set password to 'password123'
        examiner.set_password('password123')
        
        print(f"✅ Password set to: password123")
    
    db.session.commit()
    print(f"\n✅ All examiner passwords reset to 'password123'")
    
    print(f"\n📋 EXAMINER ACCOUNTS:")
    for examiner in examiners:
        print(f"  Email: {examiner.email}")
        print(f"  Password: password123")
        print()
