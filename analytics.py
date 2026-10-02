class Analytics:
    @staticmethod
    def get_today_appointments():
        return {"count": 0, "revenue": 0}
    
    @staticmethod
    def get_monthly_stats():
        return {
            "total_patients": 0,
            "new_patients": 0,
            "appointments": 0,
            "revenue": 0,
            "no_shows": 0
        }
    
    @staticmethod
    def get_doctor_performance():
        return {
            "Dr. Aisha": {"appointments": 0, "ratings": 0, "patients": 0},
            "Dr. Ahmed": {"appointments": 0, "ratings": 0, "patients": 0}
        }
