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
| 🗣️ **Natural Conversation** | OpenAI GPT-4o-mini + Realtime API |
| 📅 **Appointment Booking** | Book / cancel / list appointments |
| 🚨 **Emergency Handling** | Auto-detects emergencies → directs to 1122 / 911 |
| 💊 **Safety First** | Never suggests medicines or diagnoses |
| 📊 **Clinic Dashboard** | Live stats, patients, doctors, calls |
| 🌐 **Urdu + English** | Fully bilingual support |
| 📱 **WhatsApp / Telegram ready** | Messaging service included |
| 🗄️ **MySQL Models** | Full SQLAlchemy schema ready |

---

## 🖼️ Screenshots

### Dashboard Overview
![Dashboard](docs/screenshots/00-dashboard-main.png)

### Weekly Call Analytics + Recent Calls
![Analytics](docs/screenshots/01-dashboard-overview.png)

### Stats Cards
![Stats](docs/screenshots/02-dashboard-stats.png)

### AI Assistant Settings
![AI Settings](docs/screenshots/03-ai-assistant-settings.png)

### Knowledge Base Training + Live Playground
![Knowledge](docs/screenshots/04-ai-assistant-knowledge.png)

### Call Logs
![Call Logs](docs/screenshots/05-call-logs.png)

### Appointments
![Appointments](docs/screenshots/06-appointments.png)

### Patients Management
![Patients](docs/screenshots/07-patients.png)

### Doctors Directory
![Doctors](docs/screenshots/08-doctors.png)

### Patient Medical History
![History](docs/screenshots/09-patient-history.png)

### Knowledge Base
![KB](docs/screenshots/10-knowledge-base.png)

### Advanced Analytics
![Analytics](docs/screenshots/11-analytics.png)

### System Integrations
![Integrations](docs/screenshots/12-integrations.png)

---

## 🎬 Demo Video

**Full demo (compressed ~2 MB):** [docs/demo/dr-aisha-clinic-demo.mp4](docs/demo/dr-aisha-clinic-demo.mp4)

> Real walkthrough of the complete Dr. Aisha Clinic dashboard — Dashboard, AI Assistant, Call Logs, Appointments, Patients, Doctors, Knowledge Base, Analytics & Integrations.

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

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/ahmadraza-automation/doctor-voice-agent.git
cd doctor-voice-agent
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Environment
```bash
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxx
TWILIO_ACCOUNT_SID=ACxxxxxxxx
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
PORT=5050
PUBLIC_URL=https://your-ngrok-url.ngrok-free.app
```

### 3. Run
```bash
python main.py
```

### 4. Expose with ngrok
```bash
ngrok http 5050
```

### 5. Twilio Webhook
In Twilio Console → Phone Numbers → your number → Voice webhook:

```
POST https://YOUR-NGROK-URL.ngrok-free.app/voice/incoming
```

---

## 📁 Project Structure

```
doctor-voice-agent/
├── main.py                 # FastAPI app + Twilio + chat + WebRTC
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
├── docs/
│   ├── screenshots/        # Real UI screenshots
│   └── demo/               # Compressed demo video
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
| `GET`  | `/` | Frontend / health page |
| `POST` | `/chat` | Text chat with Dr. Aisha |
| `POST` | `/voice/incoming` | Twilio inbound call |
| `POST` | `/voice/handle` | Speech handling |
| `POST` | `/api/dial-doctor` | Outbound call to doctor |
| `GET`  | `/api/dashboard` | Full dashboard data |
| `GET`  | `/api/patients` | Patients list |
| `GET`  | `/api/doctors` | Doctors list |
| `GET`  | `/api/appointments` | Appointments |
| `POST` | `/offer` | WebRTC offer (browser calling) |
| `GET`  | `/health` | Health check |

---

## 🛠️ Tech Stack

- **Backend**: FastAPI + Uvicorn
- **Voice**: Twilio Programmable Voice
- **AI**: OpenAI GPT-4o-mini / Realtime API
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
