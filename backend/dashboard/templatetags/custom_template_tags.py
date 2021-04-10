from django import template
from golab.models import *

register = template.Library()


@register.simple_tag
def getDob(obj):
    dob = None
    for form in obj:
        for value in form['values']:
            if value['fieldID'] == 8666028:
                dob = value['value']
                break
    return dob


@register.simple_tag
def getTest(obj):
    try:
        test = Test.objects.get(acuity_appointment__acuity_appointment_id=obj)
    except Test.DoesNotExist:
        test = Test()
    return test


@register.simple_tag
def getTestFromDict(acuity_appointment_id, appointment_data):
    data = next((x for x in appointment_data if x.get('acuity_appointment_id') == acuity_appointment_id), {})
    return data.get('test', Test())


@register.simple_tag
def getTestTypeIdFromDict(acuity_appointment_id, appointment_data):
    data = next((x for x in appointment_data if x.get('acuity_appointment_id') == acuity_appointment_id), {})
    return data.get('type_ids')


@register.simple_tag
def getSendSmsNotificationFromDict(acuity_appointment_id, appointment_data):
    data = next((x for x in appointment_data if x.get('acuity_appointment_id') == acuity_appointment_id), {})
    return data


@register.simple_tag
def getTestTypes(obj):
    try:
        test = Test.objects.get(acuity_appointment__acuity_appointment_id=obj)
    except Test.DoesNotExist:
        test = None
    if test is None:
        return 'None'
    test_type_data = []
    for test_type in test.test_type.all():
        test_type_data.append(test_type.type_name)
    return ", ".join(el for el in test_type_data)


@register.simple_tag
def getTestTypeIds(obj):
    try:
        test = Test.objects.get(acuity_appointment__acuity_appointment_id=obj)
    except Test.DoesNotExist:
        test = None
    if test is None:
        return 'None'
    ids = test.test_type.all().values_list('pk', flat=True)
    return list(ids)


@register.simple_tag
def getSendSmsNotification(obj):
    try:
        appointment = AcuityAppointment.objects.get(acuity_appointment_id=obj)
        data = {"marked": appointment.send_sms_notification}
    except AcuityAppointment.DoesNotExist:
        data = {"marked": True}
    return data
