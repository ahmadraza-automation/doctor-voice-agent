# 🏥 Doctor Voice Agent — Dr. Aisha

**AI-powered voice & chat medical assistant** for clinics.  
Built with **FastAPI + Twilio + OpenAI** — handles real phone calls, appointments, and patient queries in Urdu + English.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg)](https://fastapi.tiangolo.com)
[![Twilio](https://img.shields.io/badge/Twilio-Voice-F22F46.svg)](https://twilio.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📞 **Real Phone Calls** | Inbound / outbound voice via Twilio |
| 🗣️ **Natural Conversation** | OpenAI GPT-4o-mini (fallback replies if no key) |
| 📅 **Appointment Booking** | Book / cancel / list appointments |
| 🚨 **Emergency Handling** | Auto-detects emergencies → directs to 1122 / 911 |
| 💊 **Safety First** | Never suggests medicines or diagnoses |
| 📊 **Clinic Dashboard** | Live stats, patients, doctors, calls |
| 🌐 **Urdu + English** | Fully bilingual support |
| 📱 **WhatsApp / Telegram ready** | Messaging service included |
| 🗄️ **MySQL Models** | Full SQLAlchemy schema ready |

---

## 🚀 Quick Start (Easiest)

### 1. Clone
```bash
git clone https://github.com/ahmadraza-automation/doctor-voice-agent.git
cd doctor-voice-agent
```

### 2. One-command setup

**Linux / Mac:**
```bash
chmod +x setup.sh run.sh
./setup.sh
```

**Windows:**
```bat
setup.bat
```

This creates a virtualenv, installs dependencies, and copies `.env.example` → `.env`.

### 3. Add your keys

Edit `.env`:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxx          # optional but recommended
TWILIO_ACCOUNT_SID=ACxxxxxxxx            # needed for real phone calls
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
PORT=5050
PUBLIC_URL=https://your-ngrok-url.ngrok-free.app
```

> **Tip:** Without OpenAI key the chat still works with smart fallback replies.  
> Without Twilio the web chat + dashboard still work perfectly.

### 4. Run

**Linux / Mac:**
```bash
./run.sh
```

**Windows:**
```bat
run.bat
```

Or manually:
```bash
source venv/bin/activate   # Windows: venv\Scripts\activate
python main.py
```

### 5. Open in browser
```
http://localhost:5050
```

You will see a clean chat UI. Type anything — Dr. Aisha replies.

---

## 📞 Real Phone Calls (Optional)

1. Install [ngrok](https://ngrok.com) and run:
   ```bash
   ngrok http 5050
   ```
2. Copy the `https://xxxx.ngrok-free.app` URL into `.env` as `PUBLIC_URL`.
3. Restart the server (`./run.sh`).
4. In **Twilio Console** → Phone Numbers → your number → Voice webhook:
   ```
   POST https://YOUR-NGROK-URL.ngrok-free.app/voice/incoming
   ```
5. Call your Twilio number — Dr. Aisha answers.

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Patient   │────▶│    Twilio    │────▶│  FastAPI App    │
│  (Phone)    │     │  Voice API   │     │  (main.py)      │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                  │
                       ┌──────────────────────────┼──────────────────────────┐
                       │                          │                          │
                       ▼                          ▼                          ▼
                ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
                │ OpenAI GPT  │           │ clinic_data │           │  MySQL DB   │
                │ (Realtime)  │           │  + JSON     │           │ (optional)  │
                └─────────────┘           └─────────────┘           └─────────────┘
```

---

## 📁 Project Structure

```
doctor-voice-agent/
├── main.py                 # FastAPI app + Twilio + chat + WebRTC
├── static/index.html       # Clean chat UI (works out of the box)
├── setup.sh / setup.bat    # One-command install
├── run.sh / run.bat        # One-command start
├── system_prompt.py        # Strict medical safety rules
├── clinic_data.py          # Dashboard data layer
├── clinic_store.json       # Sample patients, doctors, appointments
├── models.py               # SQLAlchemy models (MySQL ready)
├── database.py             # DB connection
├── analytics.py            # Stats helpers
├── doctors.py              # Doctor manager
├── patient_database.py     # Simple patient store
├── prescriptions.py        # Prescription helper
├── feedback.py             # Ratings
├── messaging_service.py    # WhatsApp / Telegram / SMS ready
├── tools/                  # Appointment + knowledge + web search tools
├── knowledge/              # Clinic info knowledge base
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🛡️ Safety Rules (Built-in)

- ❌ Never diagnoses
- ❌ Never suggests any medicine / dosage
- ✅ Emergency → immediately tells caller to dial **1122** (Pakistan) or **911**
- ✅ Always professional & calm tone
- ✅ Supports Urdu + English mix

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Frontend chat UI |
| `POST` | `/chat` | Text chat with Dr. Aisha |
| `POST` | `/voice/incoming` | Twilio inbound call |
| `POST` | `/voice/handle` | Speech handling |
| `POST` | `/api/dial-doctor` | Outbound call to doctor |
| `GET`  | `/api/dashboard` | Full dashboard data |
| `GET`  | `/api/patients` | Patients list |
| `GET`  | `/api/doctors` | Doctors list |
| `GET`  | `/api/appointments` | Appointments |
| `POST` | `/offer` | WebRTC offer (browser calling) |
| `GET`  | `/health` | Health check + config status |

---

## 🛠️ Tech Stack

- **Backend**: FastAPI + Uvicorn
- **Voice**: Twilio Programmable Voice
- **AI**: OpenAI GPT-4o-mini (graceful fallback if no key)
- **Data**: JSON store + optional MySQL (SQLAlchemy)
- **Optional**: aiortc (WebRTC), WhatsApp/Telegram

---

## 📌 Roadmap

- [ ] Full React / Next.js admin dashboard
- [ ] Real Google Calendar integration
- [ ] WhatsApp Business API
- [ ] Multi-doctor routing
- [ ] Call recording + transcript storage
- [ ] Patient portal

---

## 👨‍💻 Author

**Ahmad Raza**  
Python Developer | Automation Engineer  
[GitHub](https://github.com/ahmadraza-automation) · Pakistan

---

## 📄 License

MIT — free for personal & commercial use.
