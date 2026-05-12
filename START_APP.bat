@echo off
echo Starting Exam Proctoring App...
start "Docker App" cmd /k "cd /d C:\Projects\online-exam && docker-compose up"
timeout /t 10
start "Ngrok Tunnel" cmd /k "cd /d C:\Projects\online-exam && .\ngrok.exe http 80"
echo.
echo App is starting...
echo Your link: https://hangnail-slapstick-hatbox.ngrok-free.dev
echo.
pause
