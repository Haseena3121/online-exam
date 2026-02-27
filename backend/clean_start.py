"""
Clean start - removes all cache and starts fresh
"""
import os
import shutil
import sys

def clean_cache():
    """Remove all Python cache files"""
    print("Cleaning Python cache...")
    
    # Remove __pycache__ directories
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            print(f"  Removing {cache_dir}")
            shutil.rmtree(cache_dir, ignore_errors=True)
    
    # Remove .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                pyc_file = os.path.join(root, file)
                print(f"  Removing {pyc_file}")
                os.remove(pyc_file)
    
    print("✅ Cache cleaned!")
    print("\nNow run: python run.py")

if __name__ == '__main__':
    clean_cache()
