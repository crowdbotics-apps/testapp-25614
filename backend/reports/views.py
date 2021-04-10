import csv
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from dashboard.utils import appointment_csv_header
from dashboard.templatetags.custom_template_tags import getTestTypes, getTest, getDob
from users.models import User, UserProfile
from .patients.utils import get_csv_row, patient_csv_header, get_form_value, patient_csv_header_pcr, get_csv_row_pcr


@login_required()
def acuity_appointment_csv_export_view(request, queryset):
    response = HttpResponse(content_type='text/csv')
    now = datetime.now()

    response['Content-Disposition'] = 'attachment; filename="appointment-report-%s.csv"' % now.timestamp()
    writer = csv.writer(response)
    # Create the HttpResponse object with the appropriate CSV header.
    writer.writerow(appointment_csv_header)
    for appointment in queryset.all():
        test = getTest(appointment.appointment_data.get('id', None))
        row_data = [
            appointment.appointment_type,  # Appointment Type
            appointment.user.first_name,  # First Name
            appointment.user.last_name,  # Last Name
            getDob(appointment.appointment_data.get("forms", {})),  # Patient Date of Birth
            appointment.appointment_data.get('date', ''),  # Appointment date
            appointment.appointment_data.get('time', ''),  # Test Time
            getTestTypes(appointment.appointment_data.get('id')),  # Test Type
            test.test_status,  # Test Status
            test.result  # Test Results
        ]

        writer.writerow(row_data)
    return response


@login_required
def patient_csv_export_view(request, queryset):
    response = HttpResponse(content_type='text/csv')
    now = datetime.now()

    response['Content-Disposition'] = 'attachment; filename="test-report-%s.csv"' % now.timestamp()
    writer = csv.writer(response)
    # Create the HttpResponse object with the appropriate CSV header.
    writer.writerow(patient_csv_header)

    for test in queryset.all():
        date_of_birth, gender, street_address, city, state, zip_code = '', '', '', '', '', ''
        county, contact_number, last_name, first_name, patient_race, patient_ethnicity = '', '', '', '', '', ''
        user = test.acuity_appointment.user if test.acuity_appointment else User()
        user_profile = user.user_profile if hasattr(user, 'user_profile') else UserProfile()

        if test.acuity_appointment:
            appointment = test.acuity_appointment
            date_of_birth = get_form_value(appointment.appointment_data.get("forms", {}))
            gender = get_form_value(appointment.appointment_data.get("forms", {}), 8666022)
            zip_code = get_form_value(appointment.appointment_data.get("forms", {}), 8666034)
            contact_number = appointment.appointment_data.get('phone')
            street_address = get_form_value(appointment.appointment_data.get("forms", {}), 8911198)
            city = get_form_value(appointment.appointment_data.get("forms", {}), 8974651)
            state = get_form_value(appointment.appointment_data.get("forms", {}), 8974657)
            first_name = appointment.appointment_data.get('firstName')
            last_name = appointment.appointment_data.get('lastName')
            patient_race = get_form_value(appointment.appointment_data.get("forms", {}), 9257182)
            patient_ethnicity = get_form_value(appointment.appointment_data.get("forms", {}), 9257184)

        data = {
            18: first_name or user.first_name,
            19: last_name or user.last_name,
            21: gender or user_profile.gender,  # Sex at Birth
            22: date_of_birth or user_profile.date_of_birth,  # Date of Birth
            25: street_address or user_profile.street_address,  # Patient Street Address
            26: city,  # Patient City
            27: state,  # Patent State
            28: zip_code or user_profile.zip_code,  # Patient Zip code
            29: county,  # Patient County of Residence
            30: contact_number or user_profile.contact_number,  # Patient Phone Number
            35: patient_race,  # 'Patient Race'
            37: patient_ethnicity,  # 'Patient Ethnicity'
            41: test.test_type.first().type_name,  # Test Name
            43: test.get_specimen_type_display(),  # Specimen Type
            44: test.get_result_display(),  # Test Result
            45: test.collection_date,  # Specimen Collection date
        }
        row_data = get_csv_row(data)
        writer.writerow(row_data)

    return response


@login_required
def patient_csv_export_pcr_view(request, queryset):
    response = HttpResponse(content_type='text/csv')
    now = datetime.now()

    response['Content-Disposition'] = 'attachment; filename="test-report-%s.csv"' % now.timestamp()
    writer = csv.writer(response)
    # Create the HttpResponse object with the appropriate CSV header.
    writer.writerow(patient_csv_header_pcr)

    for test in queryset.all():
        date_of_birth, gender, street_address, city, state, zip_code = '', '', '', '', '', ''
        county, contact_number, last_name, first_name, patient_race, patient_ethnicity = '', '', '', '', '', ''
        test_result = test.get_result_display()
        collection_date = test.collection_date
        received_date = test.processed_date.strftime("%Y-%m-%d") if test.processed_date else ''
        result_date = test.processed_date.strftime("%Y-%m-%d") if test.processed_date else ''
        collection_location = test.location
        user = test.acuity_appointment.user if test.acuity_appointment else User()
        user_profile = user.user_profile if hasattr(user, 'user_profile') else UserProfile()
        acuity_appointment_id = ''
        if test.acuity_appointment:
            appointment = test.acuity_appointment
            acuity_appointment_id = appointment.acuity_appointment_id
            date_of_birth = get_form_value(appointment.appointment_data.get("forms", {}))
            gender = get_form_value(appointment.appointment_data.get("forms", {}), 8666022)
            zip_code = get_form_value(appointment.appointment_data.get("forms", {}), 8666034)
            contact_number = appointment.appointment_data.get('phone')
            street_address = get_form_value(appointment.appointment_data.get("forms", {}), 8911198)
            city = get_form_value(appointment.appointment_data.get("forms", {}), 8974651)
            state = get_form_value(appointment.appointment_data.get("forms", {}), 8974657)
            first_name = appointment.appointment_data.get('firstName')
            last_name = appointment.appointment_data.get('lastName')
            patient_race = get_form_value(appointment.appointment_data.get("forms", {}), 9257182)
            patient_ethnicity = get_form_value(appointment.appointment_data.get("forms", {}), 9257184)

        data = {
            1: acuity_appointment_id,
            2: first_name or user.first_name,
            3: last_name or user.last_name,
            4: date_of_birth or user_profile.date_of_birth,  # Date of Birth
            5: gender or user_profile.gender,  # Sex at Birth
            6: street_address,  # Street Address
            7: city,  # City
            8: state,  # State # Todo: fetch state from acuity data
            9: zip_code,  # zip code
            10: patient_race,  # Race
            11: patient_ethnicity,  # Patient Ethnicity
            12: collection_date,  # Collection date
            13: received_date,  # Received date
            14: result_date,  # Result date
            15: test_result,  # Test result
            16: collection_location,  # Collection location
            17: contact_number,  # Patient Telephone
            18: county
        }
        row_data = get_csv_row_pcr(data)
        writer.writerow(row_data)

    return response
