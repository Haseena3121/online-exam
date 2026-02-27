"""
Verify routes are correctly registered
"""
from app import create_app

app = create_app()

print("\nChecking proctoring routes...")
print("="*60)

proctoring_routes = []
for rule in app.url_map.iter_rules():
    if 'proctoring' in str(rule):
        proctoring_routes.append(str(rule))

print(f"Found {len(proctoring_routes)} proctoring routes:")
for route in sorted(proctoring_routes):
    print(f"  {route}")

print("\n" + "="*60)

# Check specifically for submit
submit_found = any('/submit' in r for r in proctoring_routes)
correct_path = '/api/proctoring/submit' in proctoring_routes
double_prefix = '/api/proctoring/api/proctoring/submit' in proctoring_routes

print("\nVerification:")
print(f"  Submit route exists: {submit_found}")
print(f"  Correct path (/api/proctoring/submit): {correct_path}")
print(f"  Double prefix (BUG): {double_prefix}")

if correct_path:
    print("\n✅ Routes are CORRECT!")
elif double_prefix:
    print("\n❌ Routes have DOUBLE PREFIX bug!")
    print("   Fix: Remove url_prefix from Blueprint definition")
else:
    print("\n❌ Submit route NOT FOUND!")

print("="*60)
