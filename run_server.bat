@echo off
REM Bursary System Server Startup Script
REM This script activates the virtual environment and runs the Django development server

cd /d "c:\Users\user\Documents\Finalyearproject\Bursary_system"

REM Activate virtual environment
call .\.venv\Scripts\activate.bat

REM Run Django server
python manage.py runserver 0.0.0.0:8000

pause
