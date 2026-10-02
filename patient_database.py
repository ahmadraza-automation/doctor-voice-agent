import json
from datetime import datetime

class PatientDB:
    FILE = "patients.json"
    
    @staticmethod
    def add_patient(name, phone, email, age, complaints):
        patients = PatientDB.load()
        patients[phone] = {
            "name": name,
            "phone": phone,
            "email": email,
            "age": age,
            "complaints": complaints,
            "joined": datetime.now().isoformat(),
            "appointments": []
        }
        with open(PatientDB.FILE, 'w') as f:
            json.dump(patients, f, indent=2)
        return True
    
    @staticmethod
    def load():
        try:
            with open(PatientDB.FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    @staticmethod
    def get_patient(phone):
        patients = PatientDB.load()
        return patients.get(phone)
