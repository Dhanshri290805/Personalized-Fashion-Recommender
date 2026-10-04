@echo off
echo Starting Terminal CLI...
cd "%~dp0"
call venv\Scripts\activate
python cli.py
pause
