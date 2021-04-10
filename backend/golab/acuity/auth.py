import requests
from django.conf import settings
session = requests.Session()
session.auth = (settings.ACUITY_USER_ID, settings.ACUITY_API_KEY)

