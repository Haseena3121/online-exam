@echo off
echo ========================================
echo NATIVE FRONTEND START
echo ========================================
cd frontend
echo Running npm install if needed and starting...
call npm install
npm start
pause
