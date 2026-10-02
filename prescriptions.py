import json
from datetime import datetime

class Prescriptions:
    FILE = "prescriptions.json"
    
    @staticmethod
    def create_prescription(patient_phone, medicines, instructions, doctor_name):
        prescription = {
            "id": str(datetime.now().timestamp()),
            "patient_phone": patient_phone,
            "medicines": medicines,
            "instructions": instructions,
            "doctor": doctor_name,
            "date": datetime.now().isoformat(),
            "status": "active"
        }
        prescriptions = Prescriptions.load()
        prescriptions[prescription["id"]] = prescription
        with open(Prescriptions.FILE, 'w') as f:
            json.dump(prescriptions, f, indent=2)
        return prescription
    
    @staticmethod
    def get_prescription(patient_phone):
        prescriptions = Prescriptions.load()
        for p in prescriptions.values():
            if p["patient_phone"] == patient_phone:
                return p
        return None
    
    @staticmethod
    def load():
        try:
            with open(Prescriptions.FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
