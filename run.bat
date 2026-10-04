@echo off
echo Starting Personalized Fashion Recommendation System...

echo Starting Backend...
start cmd /k "start_backend.bat"

echo Starting Frontend...
start cmd /k "start_frontend.bat"

echo Both services have been started in new windows.
pause
