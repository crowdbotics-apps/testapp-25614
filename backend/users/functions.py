from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.contrib.sites.models import Site


def send_html_verification_code(email, code):
    current_site = Site.objects.get_current()
    template_data = {
        'code': code,
        'email': email,
        'domain': current_site.domain,
    }
    html_email = get_template('users/emails/otp_email.html').render(template_data)
    subject = 'GoLab Account Verification Code'
    recipient_emails = [email, ]

    try:
        msg = EmailMessage(subject, html_email, 'noreply@golabsolutions.com', recipient_emails)
        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_emails)
        msg.content_subtype = 'html'
        msg.send()
    except:
        print('failed to send email')
