from django import template

from ..models import AcuityAppointment

register = template.Library()

from ..acuity.appointments import Appointments


@register.simple_tag
def patient_appointments_list(email):
    params = {
        'email': email
    }
    object_list = Appointments.appointment_list(params)
    return object_list


@register.simple_tag()
def user_appointment_list(user, limit=None):
    object_list = AcuityAppointment.objects.filter(user_id=user).order_by('-created')
    return object_list
