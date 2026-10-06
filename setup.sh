#!/usr/bin/env bash
set -e

echo "🏥 Dr. Aisha — Doctor Voice Agent Setup"
echo "======================================"

# Create venv if missing
if [ ! -d "venv" ]; then
  echo "→ Creating virtual environment..."
  python3 -m venv venv || python -m venv venv
fi

# Activate
source venv/bin/activate

echo "→ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# .env
if [ ! -f ".env" ]; then
  echo "→ Creating .env from .env.example..."
  cp .env.example .env
  echo ""
  echo "⚠️  IMPORTANT: Edit .env and add your keys:"
  echo "   OPENAI_API_KEY=sk-..."
  echo "   TWILIO_ACCOUNT_SID=AC..."
  echo "   TWILIO_AUTH_TOKEN=..."
  echo "   TWILIO_PHONE_NUMBER=+..."
  echo ""
else
  echo "→ .env already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. Run:   source venv/bin/activate && python main.py"
echo "  3. Open:  http://localhost:5050"
echo "  4. (Optional) ngrok http 5050  → set PUBLIC_URL in .env"
echo ""
