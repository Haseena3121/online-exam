#!/usr/bin/env python3
"""
Test the exam results endpoint to see what data is being returned
"""

from app import create_app
from database import db
from models import Exam, ExamResult, ViolationLog, User
from flask_jwt_extended import create_access_token

app = create_app()

with app.app_context():
    print("=" * 60)
    print("🧪 TESTING EXAM RESULTS ENDPOINT")
    print("=" * 60)
    
    # Get an examiner
    examiner = User.query.filter_by(role='examiner').first()
    print(f"\n👨‍🏫 Testing as examiner: {examiner.name} (ID: {examiner.id})")
    
    # Get one of their exams
    exam = Exam.query.filter_by(examiner_id=examiner.id).first()
    if not exam:
        print("❌ No exams found for this examiner")
        exit()
    
    print(f"📚 Testing exam: {exam.title} (ID: {exam.id})")
    
    # Get results for this exam
    results = ExamResult.query.filter_by(exam_id=exam.id).all()
    print(f"📊 Found {len(results)} results")
    
    # Check each result
    for result in results:
        student = User.query.get(result.student_id)
        violations = ViolationLog.query.filter_by(
            exam_id=exam.id,
            student_id=result.student_id
        ).all()
        
        print(f"\n  Student: {student.name} (ID: {student.id})")
        print(f"    Marks: {result.obtained_marks}/{result.total_marks}")
        print(f"    Violations: {len(violations)}")
        
        if len(violations) > 0:
            print(f"    Sample violations:")
            for v in violations[:3]:
                print(f"      - {v.violation_type} (Evidence: {v.evidence_path if hasattr(v, 'evidence_path') else 'None'})")
        else:
            print(f"    ⚠️  NO VIOLATIONS FOUND!")
    
    # Now simulate the API endpoint
    print(f"\n" + "=" * 60)
    print("🔍 SIMULATING API RESPONSE")
    print("=" * 60)
    
    results_data = []
    for result in results:
        student = User.query.get(result.student_id)
        violations = ViolationLog.query.filter_by(
            exam_id=exam.id,
            student_id=result.student_id
        ).order_by(ViolationLog.created_at.desc()).all()
        
        violations_list = []
        for v in violations:
            violation_dict = {
                'id': v.id,
                'type': v.violation_type,
                'severity': v.severity if hasattr(v, 'severity') and v.severity else 'medium',
                'reduction': v.trust_score_reduction,
                'evidence_path': v.evidence_path if hasattr(v, 'evidence_path') and v.evidence_path else None,
                'time': v.created_at.isoformat() if v.created_at else None
            }
            violations_list.append(violation_dict)
        
        result_dict = {
            'student': {
                'id': student.id,
                'name': student.name,
                'email': student.email
            },
            'marks': {
                'obtained': result.obtained_marks,
                'total': result.total_marks
            },
            'violation_count': len(violations),
            'violations': violations_list
        }
        results_data.append(result_dict)
    
    print(f"\n📦 API would return {len(results_data)} results")
    for r in results_data:
        print(f"\n  {r['student']['name']}:")
        print(f"    Marks: {r['marks']['obtained']}/{r['marks']['total']}")
        print(f"    Violations: {r['violation_count']}")
        if r['violation_count'] > 0:
            print(f"    First violation: {r['violations'][0]['type']}")
            print(f"    Has evidence: {r['violations'][0]['evidence_path'] is not None}")
    
    print(f"\n" + "=" * 60)
    print("✅ TEST COMPLETE")
    print("=" * 60)
