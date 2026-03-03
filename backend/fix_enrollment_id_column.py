"""
Add missing enrollment_id column to exam_results table
"""
import sqlite3

# Connect to database
conn = sqlite3.connect('exam_proctoring.db')
cursor = conn.cursor()

print("=" * 60)
print("🔧 FIXING EXAM_RESULTS TABLE - Adding enrollment_id")
print("=" * 60)

try:
    # Check if column exists
    cursor.execute("PRAGMA table_info(exam_results)")
    columns = [col[1] for col in cursor.fetchall()]
    
    print(f"\n📋 Current columns: {', '.join(columns)}")
    
    if 'enrollment_id' not in columns:
        print("\n⚠️  enrollment_id column is MISSING!")
        print("➕ Adding enrollment_id column...")
        
        cursor.execute("""
            ALTER TABLE exam_results 
            ADD COLUMN enrollment_id INTEGER
        """)
        
        conn.commit()
        print("✅ enrollment_id column added successfully!")
    else:
        print("\n✅ enrollment_id column already exists")
    
    # Verify
    cursor.execute("PRAGMA table_info(exam_results)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"\n📋 Updated columns: {', '.join(columns)}")
    
    print("\n" + "=" * 60)
    print("✅ DATABASE FIX COMPLETE!")
    print("=" * 60)
    print("Now restart the backend: python app.py")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
