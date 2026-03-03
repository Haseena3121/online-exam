@echo off
echo ============================================================
echo CLEANING AND RESTARTING BACKEND
echo ============================================================
echo.

echo Step 1: Clearing Python cache...
if exist __pycache__ rmdir /s /q __pycache__
if exist routes\__pycache__ rmdir /s /q routes\__pycache__
if exist services\__pycache__ rmdir /s /q services\__pycache__
if exist ai_models\__pycache__ rmdir /s /q ai_models\__pycache__
del /q *.pyc 2>nul
echo ✅ Cache cleared

echo.
echo Step 2: Verifying database schema...
python -c "import sqlite3; conn = sqlite3.connect('exam_proctoring.db'); cursor = conn.cursor(); cursor.execute('PRAGMA table_info(exam_results)'); cols = [c[1] for c in cursor.fetchall()]; print('✅ enrollment_id exists' if 'enrollment_id' in cols else '❌ enrollment_id MISSING'); conn.close()"

echo.
echo Step 3: Closing old sessions...
python -c "from database import db; from models import ProctoringSession; from app import create_app; app = create_app(); app.app_context().push(); sessions = ProctoringSession.query.filter_by(status='active').all(); [setattr(s, 'status', 'ended') for s in sessions]; db.session.commit(); print(f'✅ Closed {len(sessions)} old sessions')"

echo.
echo ============================================================
echo ✅ CLEANUP COMPLETE!
echo ============================================================
echo.
echo Now run: python app.py
echo.
pause
