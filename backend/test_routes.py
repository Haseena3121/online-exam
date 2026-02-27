"""
Test if routes are registered correctly
"""
from app import create_app

def test_routes():
    """List all registered routes"""
    app = create_app()
    
    print("\n📋 Registered Routes:")
    print("=" * 80)
    
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'})),
            'path': str(rule)
        })
    
    # Sort by path
    routes.sort(key=lambda x: x['path'])
    
    # Group by prefix
    exam_routes = [r for r in routes if '/exams' in r['path']]
    auth_routes = [r for r in routes if '/auth' in r['path']]
    proctoring_routes = [r for r in routes if '/proctoring' in r['path']]
    other_routes = [r for r in routes if r not in exam_routes + auth_routes + proctoring_routes]
    
    print("\n🔐 AUTH ROUTES:")
    for route in auth_routes:
        print(f"  {route['methods']:20} {route['path']}")
    
    print("\n📝 EXAM ROUTES:")
    for route in exam_routes:
        print(f"  {route['methods']:20} {route['path']}")
    
    print("\n👁️ PROCTORING ROUTES:")
    for route in proctoring_routes:
        print(f"  {route['methods']:20} {route['path']}")
    
    print("\n🔧 OTHER ROUTES:")
    for route in other_routes:
        print(f"  {route['methods']:20} {route['path']}")
    
    print("\n" + "=" * 80)
    print(f"Total routes: {len(routes)}")

if __name__ == '__main__':
    test_routes()
