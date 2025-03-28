from app.models import User


class KarvonenCalculator:
    @staticmethod
    def calculate_zones(age, resting_hr, max_hr=None):
        max_hr = max_hr or (220 - age)
        hr_reserve = max_hr - resting_hr

        return {
            'zone1': round(resting_hr + (hr_reserve * 0.5)),
            'zone2': round(resting_hr + (hr_reserve * 0.6)),
            'zone3': round(resting_hr + (hr_reserve * 0.7)),
            'zone4': round(resting_hr + (hr_reserve * 0.8)),
            'zone5': round(resting_hr + (hr_reserve * 0.9))
        }


class WearableService:
    @staticmethod
    def connect_polar(code):
        # Implementación básica de conexión con Polar
        # En producción usaría requests para interactuar con la API
        return {
            'status': 'success',
            'access_token': 'mock-access-token',
            'athlete_id': 'mock-athlete-id'
        }