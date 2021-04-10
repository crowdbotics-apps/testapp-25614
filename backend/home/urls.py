from django.urls import path
from .views import home, acuity_webhook_changed, twilio_webhook_notification_sms, user_list

urlpatterns = [
    path("", home, name="home"),
    # path("user-list/", user_list, name="user_list"),
    path("acuity/webhook/changed/", acuity_webhook_changed, name="acuity_webhook_changed"),
    path("webhook/twilio/notification/", twilio_webhook_notification_sms, name="webhook_notification_sms")
]
