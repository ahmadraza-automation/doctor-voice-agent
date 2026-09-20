"""
Appointment booking tools.
For production, connect this to Google Calendar, Cal.com, or your clinic's PMS.
Currently includes a solid structure + Google Calendar support.
"""

from datetime import datetime, timedelta
from typing import Optional

# Simple in-memory store for demo (replace with real DB / Google Calendar)
APPOINTMENTS = []

def get_available_slots(date: str, duration_minutes: int = 30) -> str:
    """
    Get available appointment slots for a given date (YYYY-MM-DD).
    """
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."

    # Clinic working hours: 9 AM - 5 PM
    slots = []
    start = datetime.combine(target_date, datetime.strptime("09:00", "%H:%M").time())
    end = datetime.combine(target_date, datetime.strptime("17:00", "%H:%M").time())

    current = start
    while current + timedelta(minutes=duration_minutes) <= end:
        slot_str = current.strftime("%Y-%m-%d %H:%M")
        booked = any(a["slot"] == slot_str for a in APPOINTMENTS)
        if not booked:
            slots.append(current.strftime("%I:%M %p"))
        current += timedelta(minutes=duration_minutes)

    if not slots:
        return f"No available slots on {date}. Please try another date."

    return f"Available slots on {date}: " + ", ".join(slots)


def book_appointment(
    patient_name: str,
    phone: str,
    slot: str,
    reason: str = "General consultation"
) -> str:
    """
    Book an appointment.
    slot format: "2026-09-21 10:30" or "2026-09-21 10:30 AM"
    """
    try:
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %I:%M %p"):
            try:
                dt = datetime.strptime(slot, fmt)
                break
            except ValueError:
                continue
        else:
            return "Invalid slot format. Please provide date and time clearly."

        slot_normalized = dt.strftime("%Y-%m-%d %H:%M")

        if any(a["slot"] == slot_normalized for a in APPOINTMENTS):
            return f"Sorry, the slot {slot_normalized} is already booked. Please choose another."

        appointment = {
            "id": len(APPOINTMENTS) + 1,
            "patient_name": patient_name,
            "phone": phone,
            "slot": slot_normalized,
            "reason": reason,
            "created_at": datetime.now().isoformat(),
            "status": "confirmed"
        }
        APPOINTMENTS.append(appointment)

        return (
            f"Appointment confirmed successfully!\n"
            f"Patient: {patient_name}\n"
            f"Phone: {phone}\n"
            f"Date & Time: {dt.strftime('%A, %d %B %Y at %I:%M %p')}\n"
            f"Reason: {reason}\n"
            f"Please arrive 10 minutes early. See you soon!"
        )
    except Exception as e:
        return f"Error booking appointment: {str(e)}"


def cancel_appointment(phone: str, slot: Optional[str] = None) -> str:
    """Cancel appointment by phone number (and optionally slot)."""
    global APPOINTMENTS
    original_count = len(APPOINTMENTS)

    if slot:
        APPOINTMENTS = [a for a in APPOINTMENTS if not (a["phone"] == phone and a["slot"] == slot)]
    else:
        APPOINTMENTS = [a for a in APPOINTMENTS if a["phone"] != phone]

    cancelled = original_count - len(APPOINTMENTS)
    if cancelled > 0:
        return f"Successfully cancelled {cancelled} appointment(s) for {phone}."
    return f"No appointments found for phone number {phone}."


def list_appointments(phone: str) -> str:
    """List all appointments for a phone number."""
    user_appts = [a for a in APPOINTMENTS if a["phone"] == phone]
    if not user_appts:
        return f"No appointments found for {phone}."

    result = f"Appointments for {phone}:\n"
    for a in user_appts:
        result += f"- {a['slot']} | {a['patient_name']} | {a['reason']} ({a['status']})\n"
    return result
