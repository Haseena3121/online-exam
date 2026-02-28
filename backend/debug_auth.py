#!/usr/bin/env python3

from app import create_app
from database import db
from models import User
from flask_jwt_extended import create_access_token
import json

app = create_app()

with app.app_context():
    print("=== DEBUGGING AUTHENTICATION ===")
    
    # Check all users
    users = User.query.all()
    print("\n📋 ALL USERS:")
    for user in users:
        print(f"  ID: {user.id}, Name: {user.name}, Email: {user.email}, Role: {user.role}")
    
    # Find examiners
    examiners = User.query.filter_by(role='examiner').all()
    print(f"\n👨‍🏫 EXAMINERS ({len(examiners)}):")
    for examiner in examiners:
        print(f"  ID: {examiner.id}, Name: {examiner.name}, Email: {examiner.email}")
        
        # Create a fresh token for this examiner
        token = create_access_token(identity=str(examiner.id))
        print(f"  Fresh Token: {token[:50]}...")
    
    # Check if there are any exams
    from models import Exam
    exams = Exam.query.all()
    print(f"\n📚 TOTAL EXAMS: {len(exams)}")
    for exam in exams:
        print(f"  ID: {exam.id}, Title: {exam.title}, Examiner ID: {exam.examiner_id}")