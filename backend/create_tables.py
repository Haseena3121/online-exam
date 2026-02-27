"""
Create all database tables
"""
from app import create_app
from database import db

def create_tables():
    """Create all tables defined in models"""
    app = create_app()
    
    with app.app_context():
        print("📊 Creating database tables...")
        
        # Create all tables
        db.create_all()
        
        print("✅ All tables created successfully!")
        
        # List all tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n📋 Tables in database ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")

if __name__ == '__main__':
    create_tables()
