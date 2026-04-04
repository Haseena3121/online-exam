"""
Clear all exam-related data: exams, questions, enrollments, results,
violations, proctoring sessions, and users (except keep the DB structure).
Run: python clear_all_data.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from database import db
from models import (
    Exam, ExamQuestion, ExamEnrollment, ExamResult,
    ViolationLog, ProctoringSession, SessionAnalytics,
    ExaminerNotification, StudentAnswer, User
)

app = create_app()

with app.app_context():
    try:
        print("Clearing all data...")

        db.session.execute(db.text("SET FOREIGN_KEY_CHECKS=0"))

        for model in [
            StudentAnswer, ViolationLog, SessionAnalytics,
            ExaminerNotification, ExamResult, ProctoringSession,
            ExamEnrollment, ExamQuestion, Exam, User
        ]:
            count = db.session.query(model).delete()
            print(f"  Deleted {count} rows from {model.__tablename__}")

        db.session.execute(db.text("SET FOREIGN_KEY_CHECKS=1"))
        db.session.commit()
        print("\n✅ All data cleared. You can now register fresh accounts.")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
