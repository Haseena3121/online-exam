@echo off
echo ========================================
echo NATIVE BACKEND START - NO DOCKER
echo ========================================
cd backend
echo Starting virtual environment and server...
call .\venv_new\Scripts\activate.bat
python run.py
pause
