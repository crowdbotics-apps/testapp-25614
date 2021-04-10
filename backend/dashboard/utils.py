appointment_csv_header = [
    'Appointment ID', 'Appointment Type', 'First Name', 'Last Name', 'Date of Birth', 'Appointment Date', 'Test Time',
    'Test Type', 'Test Status',
    'Test results'
]


def get_dob(obj):
    dob = None
    for form in obj:
        for value in form['values']:
            if value['fieldID'] == 8666028:
                dob = value['value']
                break
    return dob
