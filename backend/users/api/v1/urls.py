from django.urls import path
from .views import *

app_name = 'api_users'
urlpatterns = [
    path('patient/otp-login/', send_login_otp, name="patient_login_send_otp"),
]
