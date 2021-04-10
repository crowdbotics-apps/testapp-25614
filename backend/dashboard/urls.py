from django.urls import path

from .views import *

app_name = "dashboard"
urlpatterns = [
    path('', DashboardIndex.as_view(), name='dashboard_index'),
    path('acuity/appointments/', AppointmentList.as_view(), name='dashboard_acuity_appointments'),
    path('acuity/appointments/csv', AppointmentListCSV.as_view(), name='dashboard_acuity_appointments_csv'),
    path('acuity/appointments/<int:appointment_id>/', AppointmentDetail.as_view(),
         name='dashboard_acuity_appointment_detail'),
    path('acuity/appointment-types/', AppointmentTypes.as_view(), name='dashboard_acuity_appointment_types'),
    path('acuity/appointment-addons/', AppointmentAddons.as_view(), name='dashboard_acuity_appointment_addons'),
    path('acuity/clients/', AcuityClientList.as_view(), name='dashboard_acuity_clients'),
    path('add-edit/test-result/', AddEditTestResult.as_view(), name="add_edit_test_result"),
    path('bulk-add-edit/test-result/', BulkAddEditTestResult.as_view(), name="bulk_add_edit_test_result"),
    path('toggle/notify/', ToggleNotify.as_view(), name="toggle_notify"),
    path("notify/patient/", NotifyPatient.as_view(), name="notify_patient"),
    path("notify/patient/bulk", BulkNotifyPatient.as_view(), name="bulk_notify_patient"),
    path("patient/notifications/", PatientNotificationList.as_view(), name="patient_notifications"),
    path("patient/test/results/", AppointmentTestResults.as_view(), name="test_results"),
]
