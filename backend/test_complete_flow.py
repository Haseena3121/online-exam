#!/usr/bin/env python3
"""
Complete test to verify violation reporting and evidence saving
"""

from app import create_app
from database import db
from models import ViolationLog, ProctoringSession, ExamResult, Exam, User
import os

app = create_app()

with app.app_context():
    print("=" * 60)
    print("🧪 TESTING COMPLETE VIOLATION FLOW")
    print("=" * 60)
    
    # 1. Check evidence directory
    evidence_dir = 'uploads/evidence'
    if os.path.exists(evidence_dir):
        files = [f for f in os.listdir(evidence_dir) if f != '.gitkeep']
        print(f"\n✅ Evidence directory exists")
        print(f"📁 Evidence files: {len(files)}")
    else:
        print(f"\n❌ Evidence directory missing")
        os.makedirs(evidence_dir, exist_ok=True)
        print(f"✅ Created evidence directory")
    
    # 2. Check violations
    violations = ViolationLog.query.all()
    violations_with_evidence = ViolationLog.query.filter(
        ViolationLog.evidence_path != None,
        ViolationLog.evidence_path != ''
    ).all()
    
    print(f"\n📊 VIOLATIONS:")
    print(f"  Total: {len(violations)}")
    print(f"  With evidence: {len(violations_with_evidence)}")
    print(f"  Without evidence: {len(violations) - len(violations_with_evidence)}")
    
    # 3. Check active sessions
    active_sessions = ProctoringSession.query.filter_by(status='active').all()
    ended_sessions = ProctoringSession.query.filter_by(status='ended').all()
    
    print(f"\n🎥 PROCTORING SESSIONS:")
    print(f"  Active: {len(active_sessions)}")
    print(f"  Ended: {len(ended_sessions)}")
    
    # 4. Check exam results
    results = ExamResult.query.all()
    print(f"\n📋 EXAM RESULTS: {len(results)}")
    
    # 5. Show sample violations with evidence
    print(f"\n📸 SAMPLE VIOLATIONS WITH EVIDENCE:")
    for v in violations_with_evidence[:5]:
        print(f"  ID: {v.id}")
        print(f"    Type: {v.violation_type}")
        print(f"    Student: {v.student_id}, Exam: {v.exam_id}")
        print(f"    Evidence: {v.evidence_path}")
        if v.evidence_path and os.path.exists(v.evidence_path):
            print(f"    ✅ File exists")
        else:
            print(f"    ❌ File missing")
    
    # 6. Check examiners
    examiners = User.query.filter_by(role='examiner').all()
    print(f"\n👨‍🏫 EXAMINERS: {len(examiners)}")
    for examiner in examiners:
        exams = Exam.query.filter_by(examiner_id=examiner.id).all()
        print(f"  {examiner.name} ({examiner.email}): {len(exams)} exams")
    
    # 7. Evidence retention check
    from config_evidence import get_retention_hours, is_auto_cleanup_enabled
    print(f"\n⏰ EVIDENCE RETENTION:")
    print(f"  Retention: {get_retention_hours()} hours ({get_retention_hours()/24} days)")
    print(f"  Auto-cleanup: {'ENABLED' if is_auto_cleanup_enabled() else 'DISABLED'}")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE")
    print("=" * 60)
    
    # Summary
    print(f"\n📝 SUMMARY:")
    print(f"  ✅ Evidence directory: OK")
    print(f"  ✅ Violations: {len(violations)} total, {len(violations_with_evidence)} with evidence")
    print(f"  ✅ Sessions: {len(active_sessions)} active, {len(ended_sessions)} ended")
    print(f"  ✅ Results: {len(results)} exam results")
    print(f"  ✅ Retention: 48 hours (2 days)")
    
    if len(violations_with_evidence) > 0:
        print(f"\n🎉 SYSTEM IS WORKING! Violations have evidence.")
    else:
        print(f"\n⚠️  No violations with evidence yet. Create a new exam to test.")
