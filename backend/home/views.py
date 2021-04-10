from allauth.account.utils import setup_user_email
from allauth.utils import generate_unique_username
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.template import RequestContext
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from golab.acuity.appointments import Appointments
from golab.models import AcuityAppointment
from home.models import CustomText, HomePage
from users.models import UserProfile, PatientNotification

User = get_user_model()


def handler403(request, exception):
    response = render_to_response('error_pages/403.html')
    response.status_code = 403
    return response


def handler404(request, exception):
    response = render_to_response('error_pages/404.html')
    response.status_code = 404
    return response


def handler500(request, exception):
    response = render_to_response('error_pages/500.html')
    response.status_code = 500
    return response


def user_list(request):
    users = User.objects.prefetch_related(
        Prefetch('acuityappointment_set', to_attr='appointment_ids',
                 queryset=AcuityAppointment.objects.all().distinct())
    )
    data = {
        'users': users
    }
    return render(request, 'home/user_list.html', data)


def home(request):
    packages = [
        {'name': 'django-allauth', 'url': 'https://pypi.org/project/django-allauth/0.38.0/'},
        {'name': 'django-bootstrap4', 'url': 'https://pypi.org/project/django-bootstrap4/0.0.7/'},
        {'name': 'djangorestframework', 'url': 'https://pypi.org/project/djangorestframework/3.9.0/'},
    ]
    context = {
        'customtext': CustomText.objects.first(),
        'homepage': HomePage.objects.first(),
        'packages': packages
    }
    if request.user.is_authenticated and request.user.is_patient:
        return redirect(reverse('golab:patient_dashboard'))
    elif request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect(reverse('dashboard:dashboard_index'))
    return render(request, 'home/index.html', context)


def format_phone_number(appointment):
    """
    Add +1 to the phone number
    Args:
        appointment (list) from acuity API
    Returns:
        string formatted phone number
    """
    phone_number = appointment.get('phone', '')
    if len(phone_number) > 0:
        if '+' not in phone_number:
            phone_number = f'+1{phone_number}'
    return phone_number


@csrf_exempt
def acuity_webhook_changed(request):
    post_data = request.POST
    action = post_data['action']
    if action == 'changed' or action == 'rescheduled' or action == 'canceled' or action == 'scheduled':
        appointment = Appointments.appointment_detail(post_data['id'])
        if appointment:
            appointment_id = appointment['id']
            first_name = appointment['firstName']
            last_name = appointment['lastName']
            phone_number = format_phone_number(appointment)
            email = appointment['email'].lower()

            # try:
            #     user = User.objects.get(email=email)
            # except:
            #     user = None
            # print(user)
            try:
                user = User.objects.get(email=email)
                # user.phone_number = phone_number
                # user.first_name = first_name
                # user.last_name = last_name
                # user.save()
                print('user found')
            except User.DoesNotExist:
                print('error: not user found')
                print('creating new')
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=generate_unique_username([
                        first_name, last_name, email, 'user'
                    ]),
                    phone_number=phone_number,
                    is_patient=True,
                )
                user.save()
                setup_user_email(request, user, [])

            print(user)

            if user:
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    # user_profile.contact_number = phone_number
                    user_profile.acuity_form_data = appointment['forms']
                    user_profile.save()

                except UserProfile.DoesNotExist:
                    user_profile = UserProfile(
                        user=user,
                        contact_number=phone_number,
                        acuity_form_data=appointment['forms']
                    )
                    user_profile.save()

                try:
                    object_item = AcuityAppointment.objects.get(user=user, acuity_appointment_id=appointment_id)
                    object_item.appointment_data = appointment
                    object_item.first_name = first_name
                    object_item.last_name = last_name
                    object_item.save()
                except AcuityAppointment.DoesNotExist:
                    AcuityAppointment.objects.create(user=user, acuity_appointment_id=appointment_id,
                                                     first_name=first_name, last_name=last_name,
                                                     appointment_data=appointment)

    return HttpResponse(status=200)


@csrf_exempt
def twilio_webhook_notification_sms(request):
    print(request.POST)
    data = request.POST
    sms_sid = data.get('SmsSid')
    sms_status = data.get('SmsStatus')
    notifications = PatientNotification.objects.filter(twilio_sms_sid=sms_sid)
    if notifications:
        notifications.update(sms_status=sms_status)

    return HttpResponse(request.POST, status=200)
