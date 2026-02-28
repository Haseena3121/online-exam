@echo off
echo ========================================
echo VIOLATION EVIDENCE SYSTEM SETUP
echo ========================================
echo.

echo Step 1: Updating database schema...
cd backend
python update_database_schema.py
if errorlevel 1 (
    echo ERROR: Database update failed!
    pause
    exit /b 1
)
echo.

echo Step 2: Creating evidence upload folder...
if not exist "uploads\evidence" mkdir uploads\evidence
echo Evidence folder created: backend\uploads\evidence
echo.

echo Step 3: Setup complete!
echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo 1. Restart backend: cd backend ^&^& python app.py
echo 2. Restart frontend: cd frontend ^&^& npm start
echo 3. Test the system with a new exam
echo.
echo For detailed instructions, see:
echo - SETUP_VIOLATION_EVIDENCE.md
echo - VIOLATION_EVIDENCE_GUIDE.md
echo - EXAMINER_FEATURES_COMPLETE.md
echo.
pause
