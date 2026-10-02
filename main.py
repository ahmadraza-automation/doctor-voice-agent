from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
import os
import re
import logging
from urllib.parse import parse_qs
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
import requests
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from clinic_data import get_dashboard_data, get_patients, get_doctors, get_appointments, upsert_doctor, save_integration_settings, get_integration_settings

try:
    from aiortc import RTCPeerConnection, RTCSessionDescription
except Exception:  # pragma: no cover - optional dependency for browser calling
    RTCPeerConnection = None
    RTCSessionDescription = None

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PORT = int(os.getenv('PORT', 8000))
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
PUBLIC_URL = os.getenv('PUBLIC_URL', f'http://localhost:{PORT}')

SYSTEM_PROMPT = '''You are Dr. Aisha, a professional and caring AI medical assistant.
CRITICAL: You are NOT a real doctor. NEVER suggest medicines or diagnose.
If asked about medicine, say: "I cannot suggest medicines. Please see a real doctor."
For emergencies (chest pain, difficulty breathing, severe bleeding): Tell them to call 1122/911.
Be professional, caring, concise. Support Urdu + English.
Keep responses short (2-3 sentences max).'''

app = FastAPI()

if os.path.exists('static'):
    app.mount('/static', StaticFiles(directory='static'), name='static')


def build_assistant_reply(user_message: str) -> str:
    message = (user_message or '').strip().lower()
    if not message:
        return 'Hello! I am Dr. Aisha, your virtual medical assistant. How can I help you with your clinic today?'

    if 'appointment' in message or 'book' in message:
        return 'Certainly! I can help you book an appointment. Please share your preferred date, time, and your full name.'
    if 'hour' in message or 'timing' in message or 'time' in message:
        return 'Our clinic is open Monday to Saturday from 9:00 AM to 8:00 PM.'
    if 'fever' in message or 'pain' in message or 'sick' in message or 'health' in message:
        return 'I note your symptoms. As an AI assistant, I cannot prescribe medicines or diagnose, but I recommend consulting our specialist doctor. Would you like me to book an appointment?'
    if 'service' in message:
        return 'We offer general consultations, health screenings, pediatric care, and lab testing services.'
    if 'cancel' in message:
        return 'To cancel your appointment, please provide your registered phone number or appointment ID.'
    if 'doctor' in message:
        return 'Our clinic has Dr. Aisha Ahmed, Dr. Ahmad Hassan, and Dr. Fatima Khan. Which doctor would you like to speak with?'
    return f"Thank you for reaching out. Regarding '{user_message}', I am here to help you coordinate with our clinic and schedule visits. How else can I assist you?"


def parse_form_data(raw_body: bytes) -> dict:
    text = raw_body.decode('utf-8', errors='ignore')
    parsed = parse_qs(text, keep_blank_values=True)
    return {key: values[0] if values else '' for key, values in parsed.items()}


def normalize_phone_number(phone: str) -> str:
    clean = (phone or '').strip()
    digits = re.sub(r'\D', '', clean)
    if not digits:
        return ''

    if digits.startswith('92'):
        return f'+{digits}'
    if digits.startswith('0') and len(digits) == 11:
        return f'+92{digits[1:]}'
    if len(digits) == 10 and digits.startswith('3'):
        return f'+92{digits}'
    if digits.startswith('+'):
        return digits
    return f'+{digits}'


def place_outbound_call(doctor_name: str, phone_number: str):
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
        raise RuntimeError('Twilio is not configured. Add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER and PUBLIC_URL to the environment.')

    normalized_to = normalize_phone_number(phone_number)
    if not normalized_to:
        raise ValueError('Phone number is required to place the call.')

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    twiml_url = f"{PUBLIC_URL.rstrip('/')}/twilio/voice?doctor={doctor_name.replace(' ', '%20')}"
    call = client.calls.create(
        to=normalized_to,
        from_=TWILIO_PHONE_NUMBER,
        url=twiml_url,
        method='GET'
    )
    return {
        'status': 'queued',
        'sid': call.sid,
        'doctor': doctor_name,
        'to': normalized_to,
        'from': TWILIO_PHONE_NUMBER,
    }


@app.get('/', response_class=HTMLResponse)
async def index():
    return FileResponse('static/index.html')

@app.post('/chat')
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get('message', '').strip()

        if not user_message:
            raise HTTPException(status_code=400, detail='Empty message')

        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {OPENAI_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-4o-mini',
                    'messages': [
                        {'role': 'system', 'content': SYSTEM_PROMPT},
                        {'role': 'user', 'content': user_message}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 500
                },
                timeout=10
            )
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                reply = result['choices'][0]['message']['content']
                return JSONResponse({'reply': reply})
        except Exception:
            pass

        return JSONResponse({'reply': build_assistant_reply(user_message)})

    except Exception as e:
        logger.error(f'Chat error: {e}')
        return JSONResponse({'reply': 'Hello! I am Dr. Aisha. How can I assist you at the clinic today?'}, status_code=200)


@app.post('/voice/incoming')
async def voice_incoming(request: Request):
    form = parse_form_data(await request.body())
    caller = form.get('From', 'Unknown')
    response = VoiceResponse()
    response.say('Welcome to Dr. Aisha clinic. Please say your appointment or question after the tone.')
    response.gather(
        input='speech',
        action='/voice/handle',
        method='POST',
        timeout=5,
        speechTimeout='auto',
        hints='appointment, doctor, prescription, cancel, hours, emergency'
    )
    logger.info(f'Incoming voice call from {caller}')
    return Response(content=str(response), media_type='application/xml')


@app.get('/twilio/voice')
async def twilio_voice(request: Request):
    doctor_name = request.query_params.get('doctor', 'Doctor')
    response = VoiceResponse()
    response.say(f"Connecting you to {doctor_name}. Please wait while the clinic call is being connected.")
    response.pause(length=1)
    response.say('If you need immediate assistance, please call the clinic directly.')
    return Response(content=str(response), media_type='application/xml')


@app.post('/voice/handle')
async def voice_handle(request: Request):
    form = parse_form_data(await request.body())
    speech_result = (form.get('SpeechResult') or '').strip()
    digits = (form.get('Digits') or '').strip()
    user_message = speech_result or digits or 'hello'
    reply_text = build_assistant_reply(user_message)

    response = VoiceResponse()
    response.say(reply_text)
    response.pause(length=1)
    response.say('If you need another question, please call back or ask for an appointment.')
    return Response(content=str(response), media_type='application/xml')


@app.post('/api/dial-doctor')
async def dial_doctor(request: Request):
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    doctor_name = (payload.get('doctor_name') or payload.get('doctor') or 'Doctor').strip()
    phone_number = (payload.get('phone') or payload.get('phone_number') or '').strip()

    if not phone_number:
        raise HTTPException(status_code=400, detail='Phone number is required.')

    try:
        result = place_outbound_call(doctor_name, phone_number)
        return JSONResponse({'success': True, 'call': result})
    except RuntimeError as exc:
        logger.error(f'Twilio config missing: {exc}')
        return JSONResponse({'success': False, 'error': str(exc)}, status_code=400)
    except ValueError as exc:
        logger.error(f'Invalid phone number: {exc}')
        return JSONResponse({'success': False, 'error': str(exc)}, status_code=400)
    except Exception as exc:
        logger.exception('Outbound call failed')
        return JSONResponse({'success': False, 'error': str(exc)}, status_code=500)


@app.get('/health')
async def health():
    return {'status': 'ok', 'message': 'Dr. Aisha is ready!'}

@app.get('/api/dashboard')
async def dashboard_data():
    return get_dashboard_data()

@app.get('/api/patients')
async def patients_data():
    return get_patients()

@app.get('/api/doctors')
async def doctors_data():
    return get_doctors()

@app.get('/api/appointments')
async def appointments_data():
    return get_appointments()


@app.post('/api/doctors')
async def save_doctor(request: Request):
    payload = await request.json()
    try:
        doctor = upsert_doctor(payload)
        return JSONResponse({'success': True, 'doctor': doctor})
    except ValueError as exc:
        return JSONResponse({'success': False, 'error': str(exc)}, status_code=400)


@app.post('/api/integrations')
async def save_integration(request: Request):
    payload = await request.json()
    settings = save_integration_settings(payload)
    return JSONResponse({'success': True, 'settings': settings})


@app.get('/api/integrations')
async def integration_settings():
    return get_integration_settings()


pcs = set()


@app.post('/offer')
async def offer(request: Request):
    if RTCPeerConnection is None or RTCSessionDescription is None:
        return JSONResponse(
            {'error': 'WebRTC support is not installed. Run: pip install aiortc and restart the server.'},
            status_code=503,
        )

    try:
        params = await request.json()
        if not params:
            raise ValueError('Empty offer payload')

        offer = RTCSessionDescription(sdp=params['sdp'], type=params['type'])
        pc = RTCPeerConnection()
        pcs.add(pc)

        @pc.on('connectionstatechange')
        async def on_connection_state_change():
            logger.info(f'WebRTC connection state: {pc.connectionState}')
            if pc.connectionState == 'failed':
                await pc.close()
                pcs.discard(pc)

        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return JSONResponse({
            'sdp': pc.localDescription.sdp,
            'type': pc.localDescription.type,
        })
    except Exception as exc:
        logger.exception('WebRTC offer failed')
        return JSONResponse({'error': str(exc)}, status_code=500)


@app.on_event('shutdown')
async def shutdown_event():
    for pc in list(pcs):
        await pc.close()
    pcs.clear()


if __name__ == '__main__':
    import uvicorn
    logger.info(f'🏥 Dr. Aisha Medical Assistant started on port {PORT}')
    logger.info(f'📱 Open: http://localhost:{PORT}')
    uvicorn.run(app, host='0.0.0.0', port=PORT, log_level='info')
