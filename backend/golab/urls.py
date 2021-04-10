from django.urls import path
from .views import *

from users.views import (
    PatientLogin, PatientSignup, PatientLogout, PatientProfileUpdate, logged_patient_profile, PatientProfileInfoUpdate,
    PatientAccountForgotPassword, PatientOtpLogin, verify_otp_and_login
)

app_name = "golab"
urlpatterns = [
    path('', golab_index),
    path('patient/dashboard/', PatientDashboardIndex.as_view(), name="patient_dashboard"),
    # path('patient/login/', PatientLogin.as_view(), name="patient_login"),
    path('patient/login/', PatientOtpLogin.as_view(), name="patient_login"),
    path('patient/login/verify-otp/', verify_otp_and_login, name="patient_login_verify_otp"),
    # path('patient/login/send-otp/', send_login_otp, name="patient_login_send_otp"),
    path('patient/logout/', PatientLogout.as_view(), name="patient_logout"),
    # path('patient/register/', PatientSignup.as_view(), name="patient_signup"),
    # path('patient/forgot-password/', PatientAccountForgotPassword.as_view(), name="patient_forgot_password"),
    path('patient/profile/', logged_patient_profile, name="logged_patient_profile"),
    path('patient/profile/info/', PatientProfileInfoUpdate.as_view(), name="logged_patient_profile_info"),
    path('patient/profile/update/', PatientProfileUpdate.as_view(), name="patient_account_update"),
    # path('appointments/create/', CreateAppointment.as_view(), name="patient_appointment_create"),
    path('appointments/create/', SelectAppointmentList.as_view(), name="patient_appointment_type_select"),
    path('test/results/', TestResults.as_view(), name="test_results"),
    path('test/result/download/<int:id>/',test_result_download, name='test_result_download'),
    # path('test/result/edit/<int:id>/', EditTestView.as_view(), name="edit-test-data"),
    path('test/result/download/test/', test_result_download_test, name='test_result_download_test')
    # appointments
]