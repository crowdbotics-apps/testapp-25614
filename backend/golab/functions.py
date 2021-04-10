from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string, get_template
from django.template import Context

from django.urls import reverse
from home.twilio import twilio_send_message, twilio_send_result_message
from users.models import PatientNotification


def send_ready_stauts_for_test(instance):
    # print(instance)
    # print(instance.acuity_appointment)
    # print(instance.test_status)
    user = instance.acuity_appointment.user
    print(user)

    test_results_link = reverse('golab:test_results')
    message = 'Your GoLab test results are ready. ' \
              'Please click on this link to view your results:'

    sms_message = 'Your GoLab test results are ready. ' \
                  'Please click on this link to view your results: ' \
                  'https://{}{}.'.format(settings.DEFAULT_SITE_URL, test_results_link)

    link = 'https://{}{}.'.format(settings.DEFAULT_SITE_URL, test_results_link)
    template_data = {
        'message': message,
        'link': link
    }
    html_email = get_template('golab/emails/test_status.html').render(template_data)

    email = instance.acuity_appointment.appointment_data['email']
    phone = instance.acuity_appointment.appointment_data['phone']
    subject = 'Your GoLab Test Results Are Ready'
    recipient_emails = [email, ]
    # print(message)
    notification = PatientNotification.objects.filter(
        user=user,
        acuity_appointment=instance.acuity_appointment
    )
    if notification:
        notification = notification.first()
        notification.message = sms_message
        # notification.save()
    else:
        notification = PatientNotification(
            user=instance.acuity_appointment.user
        )
        notification.acuity_appointment = instance.acuity_appointment
        notification.message = sms_message

    # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_emails)
    if notification:
        if instance.acuity_appointment.send_sms_notification:
            try:
                message = twilio_send_result_message(phone, sms_message)
                # notification.sms_status = message.status
                notification.twilio_sms_sid = message.sid
                notification.save()
            except:
                print('failed to send sms')
                pass
        try:
            msg = EmailMessage(subject, html_email, settings.DEFAULT_FROM_EMAIL, recipient_emails)
            # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_emails)
            msg.content_subtype = 'html'
            msg.send()
            notification.email_status = True
            notification.save()

        except:
            print('failed to send email')

    notification.save()

    # print(message)
    # return message
