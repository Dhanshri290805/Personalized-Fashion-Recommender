@echo off
echo Starting Backend...
cd "%~dp0"
call venv\Scripts\activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
pause
