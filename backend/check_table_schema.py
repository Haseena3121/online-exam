import sqlite3

conn = sqlite3.connect('exam_proctoring.db')
cursor = conn.cursor()

cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='exam_results'")
result = cursor.fetchone()

if result:
    print("=" * 60)
    print("EXAM_RESULTS TABLE SCHEMA:")
    print("=" * 60)
    print(result[0])
    print("=" * 60)
else:
    print("❌ Table not found!")

conn.close()
