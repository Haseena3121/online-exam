"""
Test API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_home():
    """Test home endpoint"""
    print("\n1. Testing home endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

def test_login():
    """Test login"""
    print("\n2. Testing login...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": "skhaseena009@gmail.com", "password": "password123"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   User: {data.get('user', {}).get('name')}")
            return data.get('access_token')
        else:
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    return None

def test_exams(token):
    """Test exam list"""
    print("\n3. Testing exam list...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/exams/",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Exams found: {len(data.get('exams', []))}")
            for exam in data.get('exams', []):
                print(f"     - {exam['title']} (ID: {exam['id']}, Published: {exam['is_published']})")
        else:
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

def test_exam_start(token, exam_id=2):
    """Test exam start"""
    print(f"\n4. Testing exam start (ID: {exam_id})...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/exams/{exam_id}/start",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Session ID: {data.get('session_id')}")
            print(f"   Proctoring Session: {data.get('proctoring_session_id')}")
        else:
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == '__main__':
    print("="*60)
    print("API ENDPOINT TESTS")
    print("="*60)
    
    test_home()
    token = test_login()
    
    if token:
        test_exams(token)
        test_exam_start(token)
    else:
        print("\n❌ Could not get token, skipping authenticated tests")
    
    print("\n" + "="*60)
    print("TESTS COMPLETE")
    print("="*60)
