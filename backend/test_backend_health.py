"""
Test backend health and auto-submit functionality
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Backend is running: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Backend is not running: {str(e)}")
        return False

def test_results_endpoint():
    """Test if results endpoint is accessible"""
    try:
        # This will fail without auth, but should return 401, not crash
        response = requests.get(f"{BASE_URL}/api/results/all")
        print(f"📊 Results endpoint status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Results endpoint is working (requires auth)")
            return True
        elif response.status_code == 200:
            print("✅ Results endpoint is working")
            return True
        else:
            print(f"⚠️ Unexpected status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Results endpoint error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 BACKEND HEALTH CHECK")
    print("=" * 60)
    
    if test_backend_health():
        test_results_endpoint()
    
    print("=" * 60)
    print("If backend is running but results endpoint fails,")
    print("check the backend terminal for error messages.")
    print("=" * 60)
