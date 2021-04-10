from .auth import session
from django.conf import settings


class AcuityCalendars:
    @staticmethod
    def calendar_list():
        url = '%s/calendars' % settings.ACUITY_API_URL
        res = session.get(url)
        return res.json()
