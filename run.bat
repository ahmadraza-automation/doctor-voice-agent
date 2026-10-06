@echo off
cd /d "%~dp0"

if not exist venv (
  echo Virtualenv not found. Run setup.bat first.
  pause
  exit /b 1
)

call venv\Scripts\activate.bat

if not exist .env (
  echo .env missing. Copy .env.example to .env and add your keys.
  pause
  exit /b 1
)

echo Starting Dr. Aisha...
python main.py
