from django.conf import settings
from fcm_django.models import FCMDevice
from twilio.rest import Client
from users.models import LoginOTP

account_sid = settings.TWILIO_ACCOUNT_SID
service_id = settings.TWILIO_SERVICE_ID
# Your Auth Token from twilio.com/console
auth_token = settings.TWILIO_AUTH_TOKEN


# TODO: Manage all twilio functions in a single class and initialize the client in the class constructor
def twilio_client():
    return Client(account_sid, auth_token)


def twilio_send_verification_code(user):
    client = twilio_client()
    phone_sid = None
    email_sid = None
    if user.phone_number:
        # verification_phone = client.verify \
        #     .services(service_id) \
        #     .verifications \
        #     .create(to=str(user.phone_number), channel='sms')
        # print(verification_phone.sid)
        # phone_sid = verification_phone.sid
        try:
            verification_phone = client.verify \
                .services(service_id) \
                .verifications \
                .create(to=str(user.phone_number), channel='sms')
            # print(verification_phone.sid)
            phone_sid = verification_phone.sid
        except:
            pass
    # verification_email = client.verify \
    #     .services(service_id) \
    #     .verifications \
    #     .create(to=str(user.email), channel='email')
    # print(verification_email.sid)
    # email_sid = verification_email.sid
    try:
        verification_email = client.verify \
            .services(service_id) \
            .verifications \
            .create(to=str(user.email), channel='email')
        email_sid = verification_email.sid
    except:
        pass
    # otp_object = LoginOTP.objects.create(
    #     user=user,
    #     email_sid=email_sid,
    #     phone_sid=phone_sid
    # )
    # print(phone_sid)
    try:

        otp_object = LoginOTP.objects.get(user=user)
        otp_object.email_sid = email_sid
        otp_object.phone_sid = phone_sid
        otp_object.save()
    except LoginOTP.DoesNotExist:
        otp_object = LoginOTP.objects.create(
            user=user,
            email_sid=email_sid,
            phone_sid=phone_sid
        )
    print(otp_object)


def twilio_check_verification(otp_object, code, verification_sid):
    client = twilio_client()
    # mobile = str(otp_object.mobile)
    # user = User.objects.get(mobile_number=mobile)
    service_object = client.verify.services(service_id)
    try:
        service_channel = service_object.verifications.get(verification_sid).fetch()
    except:
        service_channel = None
    status = ''
    if service_channel is not None:
        if service_channel.channel == 'email':
            print('email')
            verification_check = service_object.verification_checks \
                .create(to=str(otp_object.user.email), code=code, verification_sid=verification_sid)
            status = verification_check.status
        elif service_channel.channel == 'sms':
            print('sms')
            verification_check = service_object.verification_checks \
                .create(to=str(otp_object.user.phone_number), code=code, verification_sid=verification_sid)
            status = verification_check.status
        # else:
        #     return False
        # verification_check = client.verify \
        #     .services(service_id) \
        #     .verification_checks \
        #     .create(to=mobile, code=code, verification_sid=verification_sid, amount="10")
        #
        # print('checking_status: ', verification_check.status)
        print(status)
        if status == 'approved':
            return True

    return False


def twilio_verification_status_update(sid, status):
    client = twilio_client()
    try:
        client.verify.services(service_id).verifications.get(sid).update(
            status=status)
    except:
        pass


def twilio_number_lookups(mobile):
    client = twilio_client()
    try:
        client.lookups.phone_numbers(str(mobile)).fetch()
        return True
    except:
        return False


def twilio_send_message(phone_number, message):
    client = twilio_client()
    # twilio_message = client.messages.create(
    #     body=str(message),
    #     from_=str(settings.TWILIO_MOBILE_NUMBER),
    #     to=str(phone_number)
    # )
    try:
        twilio_message = client.messages.create(
            body=str(message),
            from_=str(settings.TWILIO_MOBILE_NUMBER),
            to=str(phone_number)
        )
    except:
        pass


def twilio_send_result_message(phone_number, message):
    client = twilio_client()
    status_callback_url = 'https://{}/webhook/twilio/notification/'.format(settings.DEFAULT_SITE_URL)
    return client.messages.create(
        body=str(message),
        from_=str(settings.TWILIO_MOBILE_NUMBER),
        status_callback=status_callback_url,
        to=str(phone_number)
    )
