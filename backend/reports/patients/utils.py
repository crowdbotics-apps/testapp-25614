patient_csv_header = [
    'Submitter Name', 'Submitted Date', 'Facility Name', 'Facility License Number', 'Facility Address',
    'Facility State', 'Facility Zip Code', 'Facility County', 'Facility Phone', 'Type of facility',
    'Other facility type specify', 'Ordering Provider Name', 'Ordering Provider Phone',
    'NPI', 'Ordering Provider Address', 'Ordering Provider City', 'Ordering Provider Zip Code',
    'Ordering Provider County', 'Patient First Name', 'Patient Last Name', 'Patient Middle Name/Initial',
    'Sex at Birth', 'Date of Birth', 'Age in years', 'Affiliation to Facility', 'Patient Street Address',
    'Patient City', 'Patient State', 'Patient Zip Code', 'Patient County of Residence',
    'Patient Phone Number', 'Is patient pregnant?', 'Did patient have symptoms of COVID-19 at time of testing?',
    'Did the patient die?', 'Date of Death (If Applicable)', 'Patient Race', 'Specify other race', 'Patient Ethnicity',
    'Patient Identifier', 'Patient Identifier Type', 'Specify other patient identifier', 'Test Name',
    'Specify other test name',
    'Specimen Type', 'Test Result', 'Specimen Collection Date', 'Device Identifier', 'Specimen ID'
]

patient_csv_header_pcr = [
    'Sample ID', 'First Name', 'Last Name', 'Date of Birth', 'Gender',
    'Street Address', 'City', 'State', 'Zip Code', 'Race', 'Ethnicity', 'Collection Date', 'Received Date',
    'Result Date', 'Test Result', 'Collection location', 'Patient Telephone', 'County'
]

patient_csv_row = [''] * 49
patient_csv_row_pcr = [''] * 18


def get_csv_row_pcr(patient_data):
    row_data = patient_csv_row_pcr.copy()
    for key, value in patient_data.items():
        row_data[key-1] = value

    return row_data


def get_csv_row(patient_data):
    row_data = patient_csv_row.copy()
    for key, value in patient_data.items():
        row_data[key] = value
    return row_data


def get_form_value(obj, field_id=8666028):
    value_ = None
    for form in obj:
        for value in form.get('values', []):
            if value.get('fieldID') == field_id:
                value_ = value['value']
                break
    return value_
