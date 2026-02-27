"""
Test submit endpoint
"""
import requests

# First login
print("1. Logging in...")
login_response = requests.post(
    "http://localhost:5000/api/auth/login",
    json={"email": "skhaseena009@gmail.com", "password": "password123"}
)

if login_response.status_code != 200:
    print(f"Login failed: {login_response.status_code}")
    print(login_response.json())
    exit(1)

token = login_response.json()['access_token']
print(f"Token: {token[:20]}...")

# Start exam
print("\n2. Starting exam...")
start_response = requests.post(
    "http://localhost:5000/api/exams/2/start",
    headers={"Authorization": f"Bearer {token}"}
)

if start_response.status_code != 200:
    print(f"Start failed: {start_response.status_code}")
    print(start_response.json())
    exit(1)

print(f"Session ID: {start_response.json()['session_id']}")

# Submit exam
print("\n3. Submitting exam...")
submit_response = requests.post(
    "http://localhost:5000/api/proctoring/submit",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "answers": [
            {"question_id": 1, "selected_answer": "a"},
            {"question_id": 2, "selected_answer": "b"},
            {"question_id": 3, "selected_answer": "c"}
        ]
    }
)

print(f"Status: {submit_response.status_code}")
print(f"Response: {submit_response.json()}")
