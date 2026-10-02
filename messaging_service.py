"""
Messaging Service - WhatsApp, Telegram, SMS
Numbers add hote hain jab doctor dey
"""

import os
from dotenv import load_dotenv

load_dotenv()

class MessagingService:
    """Universal messaging for doctor agent"""
    
    @staticmethod
    def send_appointment_notification(patient_name, patient_number, date, time):
        """Send appointment notification"""
        message = f"""
✅ Appointment Confirmed!

Patient: {patient_name}
📅 Date: {date}
⏰ Time: {time}

Thank you!
        """
        print(f"[NOTIFICATION] {patient_name}: {message}")
        # WhatsApp/Telegram/SMS hoga jab number ho
        return True
    
    @staticmethod
    def notify_doctor_new_booking(patient_name, date, time, reason=""):
        """Notify doctor of new booking"""
        message = f"""
🔔 New Appointment!

Patient: {patient_name}
📅 {date} at {time}
Reason: {reason or 'General consultation'}
        """
        print(f"[DOCTOR ALERT] {message}")
        # WhatsApp hoga jab number ho
        return True
    
    @staticmethod
    def send_reminder(patient_number, date, time):
        """Send reminder 24 hours before"""
        message = f"📅 Reminder: Appointment tomorrow at {time}"
        print(f"[REMINDER] {patient_number}: {message}")
        return True
    
    @staticmethod
    def send_urgent_alert(message_text):
        """Send urgent alert to doctor"""
        print(f"[URGENT] {message_text}")
        return True
