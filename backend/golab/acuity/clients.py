from .auth import session
from django.conf import settings


class AcuityClients:
    @staticmethod
    def client_list():
        url = '%s/clients' % settings.ACUITY_API_URL
        res = session.get(url)
        return res.json()
