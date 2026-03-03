#!/usr/bin/env python3
"""Test violation API endpoint"""

import requests
import json

def test_violation():
    """Test the violation endpoint"""
    
    # First, login as a student to get a token
    print("🔐 Logging in as student...")
    login_response = requests.post('http://localhost:5000/api/auth/login', json={
        'email': 'student@test.com',
        'password': 'password123'
    })
    
    if not login_response.ok:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return
    
    token = login_response.json()['access_token']
    print(f"✅ Logged in successfully")
    
    # Check if there's an active session
    print("\n📊 Checking for active session...")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Try to report a violation
    print("\n📝 Reporting test violation...")
    violation_data = {
        'violation_type': 'test_violation',
        'severity': 'high'
    }
    
    response = requests.post(
        'http://localhost:5000/api/proctoring/violation',
        headers=headers,
        data=violation_data
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.ok:
        data = response.json()
        print(f"✅ Violation reported successfully!")
        print(f"   Trust score: {data.get('current_trust_score')}%")
        print(f"   Response: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Failed to report violation")
        print(f"   Response: {response.text}")

if __name__ == '__main__':
    test_violation()
