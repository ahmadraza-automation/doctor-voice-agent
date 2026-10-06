@echo off
echo 🏥 Dr. Aisha — Doctor Voice Agent Setup
echo ======================================

if not exist venv (
  echo → Creating virtual environment...
  python -m venv venv
)

call venv\Scripts\activate.bat

echo → Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

if not exist .env (
  echo → Creating .env from .env.example...
  copy .env.example .env
  echo.
  echo ⚠️  IMPORTANT: Edit .env and add your keys:
  echo    OPENAI_API_KEY=sk-...
  echo    TWILIO_ACCOUNT_SID=AC...
  echo    TWILIO_AUTH_TOKEN=...
  echo    TWILIO_PHONE_NUMBER=+...
  echo.
) else (
  echo → .env already exists
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo   1. Edit .env with your API keys
echo   2. Run:   venv\Scripts\activate ^&^& python main.py
echo   3. Open:  http://localhost:5050
echo   4. (Optional) ngrok http 5050  → set PUBLIC_URL in .env
echo.
pause
