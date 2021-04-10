from django.urls import path
from .views import *

app_name = 'api_dashboard'
urlpatterns = [
    path('appointments/<int:appointment_id>/', AcuityAppointmentDetail.as_view(), name='appointment_detail'),
    path('pull-appointments/', PullAppointments.as_view(), name='pull_appointments')
]
