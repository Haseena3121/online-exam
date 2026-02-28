#!/usr/bin/env python3
"""
Test the exam results API endpoint directly
"""

from app import create_app
from flask import json

app = create_app()

with app.test_client() as client:
    # Login as examiner first
    login_response = client.post('/api/auth/login', 
        json={
            'email': 'harini1@gmail.com',
            'password': 'password123'
        }
    )
    
    print("=== LOGIN TEST ===")
    print(f"Status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        login_data = json.loads(login_response.data)
        token = login_data.get('access_token')
        user = login_data.get('user')
        
        print(f"✅ Login successful")
        print(f"User: {user.get('name')} ({user.get('role')})")
        print(f"Token: {token[:50]}...")
        
        # Now test the results endpoint
        print("\n=== EXAM RESULTS TEST ===")
        
        # Test exam 4 (maths)
        exam_id = 4
        results_response = client.get(f'/api/exams/{exam_id}/results',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        print(f"Endpoint: /api/exams/{exam_id}/results")
        print(f"Status: {results_response.status_code}")
        
        if results_response.status_code == 200:
            results_data = json.loads(results_response.data)
            print(f"✅ Results fetched successfully")
            print(f"\nExam: {results_data['exam']['title']}")
            print(f"Total Students: {results_data['total_students']}")
            print(f"Results: {len(results_data['results'])}")
            
            if len(results_data['results']) > 0:
                result = results_data['results'][0]
                print(f"\nFirst Result:")
                print(f"  Student: {result['student']['name']}")
                print(f"  Marks: {result['marks']['obtained']}/{result['marks']['total']}")
                print(f"  Trust Score: {result['trust_score']}%")
                print(f"  Violations: {result['violation_count']}")
                
                if result['violation_count'] > 0:
                    print(f"\n  Sample Violations:")
                    for v in result['violations'][:3]:
                        print(f"    - {v['type']} (Severity: {v['severity']}, Reduction: -{v['reduction']}%)")
                        if v.get('evidence_url'):
                            print(f"      Evidence: {v['evidence_url']}")
                else:
                    print(f"  ⚠️  No violations in response!")
        else:
            print(f"❌ Failed to fetch results")
            print(f"Response: {results_response.data}")
    else:
        print(f"❌ Login failed")
        print(f"Response: {login_response.data}")
