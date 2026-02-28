#!/usr/bin/env python3

from app import create_app
from database import db
from models import ViolationLog
import os
import shutil

app = create_app()

def create_dummy_evidence():
    """Create dummy evidence files for testing"""
    
    # Create evidence directory if it doesn't exist
    evidence_dir = "uploads/evidence"
    os.makedirs(evidence_dir, exist_ok=True)
    
    # Create dummy image file
    dummy_image_content = b"DUMMY_IMAGE_DATA_FOR_TESTING"
    dummy_video_content = b"DUMMY_VIDEO_DATA_FOR_TESTING"
    
    # Create test files
    test_files = []
    for i in range(5):
        # Create image file
        img_filename = f"violation_{i+1}_image.jpg"
        img_path = os.path.join(evidence_dir, img_filename)
        with open(img_path, 'wb') as f:
            f.write(dummy_image_content)
        test_files.append(img_path)
        
        # Create video file
        vid_filename = f"violation_{i+1}_video.mp4"
        vid_path = os.path.join(evidence_dir, vid_filename)
        with open(vid_path, 'wb') as f:
            f.write(dummy_video_content)
        test_files.append(vid_path)
    
    return test_files

with app.app_context():
    print("=== ADDING TEST EVIDENCE ===")
    
    # Create dummy evidence files
    test_files = create_dummy_evidence()
    print(f"✅ Created {len(test_files)} test evidence files")
    
    # Get first 10 violations without evidence
    violations = ViolationLog.query.filter(
        (ViolationLog.evidence_path == None) | (ViolationLog.evidence_path == '')
    ).limit(10).all()
    
    print(f"📊 Found {len(violations)} violations without evidence")
    
    # Add evidence paths to violations
    for i, violation in enumerate(violations):
        if i < len(test_files):
            violation.evidence_path = test_files[i]
            print(f"✅ Added evidence to violation {violation.id}: {violation.violation_type}")
    
    # Commit changes
    db.session.commit()
    print("✅ Database updated with test evidence")
    
    # Verify
    violations_with_evidence = ViolationLog.query.filter(
        ViolationLog.evidence_path != None,
        ViolationLog.evidence_path != ''
    ).count()
    
    print(f"📈 Total violations with evidence: {violations_with_evidence}")
    print("🎉 Test evidence added successfully!")
    print("\n🎯 Now refresh your examiner dashboard to see evidence display!")