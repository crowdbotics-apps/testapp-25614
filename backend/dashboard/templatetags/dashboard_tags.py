import datetime

from django import template

from golab.acuity.appointments import Appointments
from golab.acuity.calenders import AcuityCalendars

register = template.Library()


@register.simple_tag
def appointment_types():
    return Appointments.appointment_types()


@register.simple_tag
def calender_list():
    return AcuityCalendars.calendar_list()


@register.simple_tag
def make_string(value):
    return str(value)


def print_acuity_timestamp(timestamp):
    json_time_stamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')
    return json_time_stamp


register.filter(print_acuity_timestamp)
