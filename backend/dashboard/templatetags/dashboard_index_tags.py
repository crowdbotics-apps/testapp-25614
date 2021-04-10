import datetime

from django import template

from golab.acuity.appointments import Appointments

register = template.Library()


@register.simple_tag
def latest_appointments():
    params = {
        'max': 10
    }
    return Appointments.appointment_list(params)


def print_acuity_timestamp(timestamp):
    json_time_stamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')
    return json_time_stamp


register.filter(print_acuity_timestamp)
