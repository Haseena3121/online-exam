"""
Reset user passwords to known values
"""
from app import create_app
from database import db
from models import User

def reset_passwords():
    """Reset all user passwords to 'password123'"""
    app = create_app()
    
    with app.app_context():
        users = User.query.all()
        
        print(f"\n📋 Resetting passwords for {len(users)} users...")
        print("="*60)
        
        for user in users:
            user.set_password('password123')
            print(f"✅ {user.email} ({user.role}) → password123")
        
        db.session.commit()
        
        print("="*60)
        print("\n✅ All passwords reset to: password123")
        print("\nTest Accounts:")
        for user in users:
            print(f"  - {user.email} / password123 ({user.role})")

if __name__ == '__main__':
    reset_passwords()
