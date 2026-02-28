#!/usr/bin/env python3
"""
Check evidence files and retention status
"""
import os
import sqlite3
from datetime import datetime, timedelta
from config_evidence import EVIDENCE_RETENTION_HOURS, EVIDENCE_DIR

print("=" * 70)
print("📸 EVIDENCE RETENTION CHECK")
print("=" * 70)

# Check configuration
print(f"\n⚙️ Configuration:")
print(f"   Retention Period: {EVIDENCE_RETENTION_HOURS} hours ({EVIDENCE_RETENTION_HOURS/24:.1f} days)")
print(f"   Evidence Directory: {EVIDENCE_DIR}")

# Check if directory exists
if not os.path.exists(EVIDENCE_DIR):
    print(f"\n❌ Evidence directory not found: {EVIDENCE_DIR}")
    print("   Creating directory...")
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    print("   ✅ Directory created")
else:
    print(f"\n✅ Evidence directory exists")

# Check files in directory
print(f"\n📁 Files in evidence directory:")
files = [f for f in os.listdir(EVIDENCE_DIR) if f != '.gitkeep' and os.path.isfile(os.path.join(EVIDENCE_DIR, f))]

if not files:
    print("   No evidence files found")
else:
    now = datetime.now()
    cutoff = now - timedelta(hours=EVIDENCE_RETENTION_HOURS)
    
    total_size = 0
    files_by_age = {'< 24h': 0, '24-48h': 0, '> 48h': 0}
    
    print(f"   Total files: {len(files)}")
    print(f"\n   Recent files:")
    
    for i, filename in enumerate(sorted(files, key=lambda x: os.path.getmtime(os.path.join(EVIDENCE_DIR, x)), reverse=True)[:10]):
        filepath = os.path.join(EVIDENCE_DIR, filename)
        file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        file_size = os.path.getsize(filepath)
        age = now - file_time
        
        total_size += file_size
        
        # Categorize by age
        if age < timedelta(hours=24):
            files_by_age['< 24h'] += 1
            age_indicator = '🟢'
        elif age < timedelta(hours=48):
            files_by_age['24-48h'] += 1
            age_indicator = '🟡'
        else:
            files_by_age['> 48h'] += 1
            age_indicator = '🔴'
        
        if i < 5:  # Show first 5 files
            print(f"   {age_indicator} {filename}")
            print(f"      Age: {age.total_seconds() / 3600:.1f} hours")
            print(f"      Size: {file_size / 1024:.1f} KB")
            print(f"      Created: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if len(files) > 5:
        print(f"   ... and {len(files) - 5} more files")
    
    print(f"\n   📊 Files by age:")
    print(f"      🟢 < 24 hours: {files_by_age['< 24h']}")
    print(f"      🟡 24-48 hours: {files_by_age['24-48h']}")
    print(f"      🔴 > 48 hours: {files_by_age['> 48h']} (ready for cleanup)")
    
    print(f"\n   💾 Storage:")
    print(f"      Total size: {total_size / 1024 / 1024:.2f} MB")

# Check database
print(f"\n🗄️ Database check:")
db_path = 'instance/exam_proctoring.db'

if not os.path.exists(db_path):
    print(f"   ❌ Database not found: {db_path}")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Count violations with evidence
        cursor.execute("SELECT COUNT(*) FROM violations WHERE evidence_path IS NOT NULL")
        with_evidence = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM violations")
        total_violations = cursor.fetchone()[0]
        
        print(f"   Total violations: {total_violations}")
        print(f"   With evidence: {with_evidence}")
        print(f"   Without evidence: {total_violations - with_evidence}")
        
        if with_evidence > 0:
            # Show recent violations with evidence
            cursor.execute("""
                SELECT id, violation_type, evidence_path, created_at 
                FROM violations 
                WHERE evidence_path IS NOT NULL 
                ORDER BY created_at DESC 
                LIMIT 5
            """)
            
            print(f"\n   Recent violations with evidence:")
            for row in cursor.fetchall():
                vid, vtype, path, created = row
                print(f"      ID {vid}: {vtype}")
                print(f"         Path: {path}")
                print(f"         Time: {created}")
                
                # Check if file exists
                if path:
                    filename = path.split('/')[-1]
                    filepath = os.path.join(EVIDENCE_DIR, filename)
                    if os.path.exists(filepath):
                        print(f"         Status: ✅ File exists")
                    else:
                        print(f"         Status: ❌ File missing!")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Database error: {str(e)}")

# Recommendations
print(f"\n💡 Recommendations:")

if files:
    old_files = files_by_age['> 48h']
    if old_files > 0:
        print(f"   ⚠️ {old_files} files are older than 48 hours")
        print(f"   Run cleanup: python cleanup_evidence.py")
    else:
        print(f"   ✅ All files are within retention period")
    
    if total_size > 500 * 1024 * 1024:  # 500 MB
        print(f"   ⚠️ Storage usage is high ({total_size / 1024 / 1024:.2f} MB)")
        print(f"   Consider running cleanup or increasing storage")
else:
    print(f"   ℹ️ No evidence files found")
    print(f"   This is normal if no exams have been taken yet")

print("\n" + "=" * 70)
print("✅ Check complete!")
print("=" * 70)
