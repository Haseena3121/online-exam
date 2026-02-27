@echo off
echo ========================================
echo RESTARTING BACKEND WITH CLEAN CACHE
echo ========================================
echo.

echo Step 1: Cleaning Python cache...
python clean_start.py

echo.
echo Step 2: Verifying routes...
python verify_routes.py

echo.
echo Step 3: Testing submit endpoint...
python test_submit.py

echo.
echo ========================================
echo If all tests passed, backend is ready!
echo Now starting backend server...
echo ========================================
echo.
python run.py
