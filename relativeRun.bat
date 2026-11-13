@echo off
set PYTHONUNBUFFERED=1

cd /d "%~dp0"

".venv\Scripts\python.exe" "postImage.py"

pause