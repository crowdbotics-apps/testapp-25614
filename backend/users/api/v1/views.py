from random import randint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, PBKDF2PasswordHasher
from django.core.mail import send_mail
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.twilio import twilio_send_verification_code, twilio_number_lookups, twilio_send_message
from users.functions import send_html_verification_code
from users.models import LoginOTP

User = get_user_model()


def send_otp_to_user(otp, user):
    message = 'Your GoLab verification code is %s' % otp
    if user.phone_number:
        twilio_send_message(user.phone_number, message)
    try:
        send_html_verification_code(user.email, otp)
    except:
        pass


@api_view(['POST'])
def send_login_otp(request):
    username = request.data.get('username').lower()
    # user = User.objects.filter(email=username)
    try:
        # user = User.objects.filter(Q(email=username) | Q(phone_number=username))
        user = User.objects.get(email=username)
    except User.DoesNotExist:
        return Response({'message': 'No user found- your email does not match our records.'},
                        status=status.HTTP_404_NOT_FOUND)
    if user:
        rand = randint(100000, 999999)
        otp_hash = make_password(rand, salt=settings.SECRET_KEY)
        # otp_hash = PBKDF2PasswordHasher(rand)
        print(user.phone_number)

        success_message = 'Verification code has been emailed to you. Enter code here.'
        error_message = 'Verification code send error. Contact support.'
        if user.phone_number:
            success_message = 'Verification code has been emailed and texted to you. Enter code here.'
            # number_valid = twilio_number_lookups(user.phone_number)
            # if number_valid:
            #     success_message = 'Verification code has been emailed and texted to you. Enter code here.'
        try:
            LoginOTP.objects.filter(user=user).delete()
            LoginOTP.objects.create(user=user, otp_hash=otp_hash)
            send_otp_to_user(rand, user)
            # twilio_send_verification_code(user)
            return Response({'message': success_message}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)
