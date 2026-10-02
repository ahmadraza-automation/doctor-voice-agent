class DoctorManager:
    DEFAULT_DOCTORS = {
        "dr_aisha": {
            "name": "Dr. Aisha",
            "specialty": "General Medicine",
            "phone": "",
            "availability": "9AM-5PM",
            "rating": 4.8
        },
        "dr_ahmed": {
            "name": "Dr. Ahmed",
            "specialty": "Cardiology",
            "phone": "",
            "availability": "10AM-6PM",
            "rating": 4.6
        }
    }
    
    @staticmethod
    def get_all_doctors():
        return DoctorManager.DEFAULT_DOCTORS
    
    @staticmethod
    def get_doctor(doctor_id):
        return DoctorManager.DEFAULT_DOCTORS.get(doctor_id)
