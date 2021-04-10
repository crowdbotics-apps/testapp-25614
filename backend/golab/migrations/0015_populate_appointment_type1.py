from django.db import migrations
from golab.models import AcuityAppointment
from golab.acuity.appointments import Appointments


def populate_appointment_type(_, __):
    """
    Populated the new appointment_type field with appropriate acuity type name
    """
    pass
    # try:
    #     appointment_types = Appointments.appointment_types()
    #     appointment_type = ''
    #     for appointment in AcuityAppointment.objects.all():
    #         appointment_type_id = appointment.appointment_data.get('appointmentTypeID', '')
    #         for item in appointment_types:
    #             if item.get('id') == appointment_type_id:
    #                 appointment_type = item.get('name', '')
    #                 break
    #         appointment.appointment_type = appointment_type
    #         appointment.save()
    # except:
    #     pass


class Migration(migrations.Migration):
    dependencies = [
        ('golab', '0014_acuityappointment_appointment_type'),
    ]

    operations = [
        # migrations.RunPython(populate_appointment_type, reverse_code=migrations.RunPython.noop)
    ]
