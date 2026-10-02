import json
from datetime import datetime

class Feedback:
    FILE = "feedback.json"
    
    @staticmethod
    def add_rating(patient_phone, doctor_name, rating, comment):
        feedback = {
            "patient": patient_phone,
            "doctor": doctor_name,
            "rating": rating,
            "comment": comment,
            "date": datetime.now().isoformat()
        }
        all_feedback = Feedback.load()
        all_feedback.append(feedback)
        with open(Feedback.FILE, 'w') as f:
            json.dump(all_feedback, f, indent=2)
        return True
    
    @staticmethod
    def get_doctor_rating(doctor_name):
        all_feedback = Feedback.load()
        ratings = [f["rating"] for f in all_feedback if f["doctor"] == doctor_name]
        return sum(ratings) / len(ratings) if ratings else 0
    
    @staticmethod
    def load():
        try:
            with open(Feedback.FILE, 'r') as f:
                return json.load(f)
        except:
            return []
