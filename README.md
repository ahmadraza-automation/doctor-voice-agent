# Doctor Voice Agent (Twilio + OpenAI Realtime)

Pure custom full phone-call system.

**Features:**
- Real-time inbound phone conversations
- Appointment booking / cancel / list
- Emergency handling (strict)
- Never suggests medicines
- Knowledge base + web search tools

## Setup

```bash
git clone https://github.com/ahmadraza-automation/doctor-voice-agent.git
cd doctor-voice-agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Mac/Linux activate: `source venv/bin/activate`

Edit `.env` with your OpenAI + Twilio keys, then:

```bash
python main.py
```

Expose with ngrok:

```bash
ngrok http 5050
```

Twilio webhook (POST):
`https://YOUR-NGROK-URL.ngrok-free.app/incoming-call`
