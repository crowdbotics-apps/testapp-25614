from .auth import session
from django.conf import settings


class AcuityCreate:
    @staticmethod
    def create_addons():
        url = '%s/appointments' % settings.ACUITY_API_URL
        res = session.get(url)
        return res.json()

