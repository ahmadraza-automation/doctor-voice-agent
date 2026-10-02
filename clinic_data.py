import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORE_PATH = BASE_DIR / 'clinic_store.json'


def _load_store():
    with STORE_PATH.open('r', encoding='utf-8') as fh:
        return json.load(fh)


def _write_store(data):
    with STORE_PATH.open('w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=2)
        fh.write('\n')


def _refresh_globals():
    global DATA, DOCTORS, PATIENTS, APPOINTMENTS, RECENT_CALLS, WEEKLY_CALLS
    DATA = _load_store()
    DOCTORS = DATA.get('doctors', [])
    PATIENTS = DATA.get('patients', [])
    APPOINTMENTS = DATA.get('appointments', [])
    RECENT_CALLS = DATA.get('recent_calls', [])
    WEEKLY_CALLS = DATA.get('weekly', [])


DATA = _load_store()
DOCTORS = DATA.get('doctors', [])
PATIENTS = DATA.get('patients', [])
APPOINTMENTS = DATA.get('appointments', [])
RECENT_CALLS = DATA.get('recent_calls', [])
WEEKLY_CALLS = DATA.get('weekly', [])


def get_dashboard_data():
    return {
        "stats": DATA.get('stats', []),
        "weekly": WEEKLY_CALLS,
        "recent_calls": RECENT_CALLS,
        "patients": PATIENTS,
        "doctors": DOCTORS,
        "appointments": APPOINTMENTS,
    }


def get_patients():
    return PATIENTS


def get_doctors():
    return DOCTORS


def get_appointments():
    return APPOINTMENTS


def upsert_doctor(doctor_payload):
    payload = dict(doctor_payload or {})
    name = (payload.get('name') or '').strip()
    if not name:
        raise ValueError('Doctor name is required.')

    doctors = list(DATA.get('doctors', []))
    existing_index = next((idx for idx, doc in enumerate(doctors) if doc.get('name') == name), None)

    if existing_index is not None:
        doctors[existing_index].update(payload)
        saved = doctors[existing_index]
    else:
        saved = {
            'id': payload.get('id') or f"doc_{len(doctors) + 1}",
            'name': name,
            'specialty': payload.get('specialty') or 'General Medicine',
            'phone': payload.get('phone') or '+92 300 0000000',
            'availability': payload.get('availability') or 'Mon-Sat: 9:00 AM - 5:00 PM',
            'rating': payload.get('rating') or 4.8,
            'is_active': payload.get('is_active', True),
        }
        doctors.append(saved)

    DATA['doctors'] = doctors
    _write_store(DATA)
    _refresh_globals()
    return saved


def save_integration_settings(settings_payload):
    payload = dict(settings_payload or {})
    DATA['integrations'] = {
        'api_key': payload.get('api_key') or payload.get('apiKey') or '',
        'webhook_url': payload.get('webhook_url') or payload.get('webhookUrl') or '',
        'google_calendar_connected': payload.get('google_calendar_connected', payload.get('googleCalendarConnected', False)),
    }
    _write_store(DATA)
    _refresh_globals()
    return DATA['integrations']


def get_integration_settings():
    return DATA.get('integrations', {})
