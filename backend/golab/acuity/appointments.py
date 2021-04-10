import urllib.parse
from .auth import session
from django.conf import settings


class Appointments:
    @staticmethod
    def appointment_list(parmas):
        max = 100
        email = ''
        firstName = ''
        lastName = ''
        phone = ''
        minDate = ''
        maxDate = ''
        appointmentTypeID = ''
        calendarID = ''
        direction = ''
        if 'max' in parmas:
            max = parmas['max']
        if 'email' in parmas:
            email = parmas['email']
        if 'firstName' in parmas:
            firstName = parmas['firstName']
        if 'lastName' in parmas:
            lastName = parmas['lastName']
        if 'phone' in parmas:
            phone = parmas['phone']
            if phone:
                phone = urllib.parse.quote(phone) if '+' in phone else urllib.parse.quote(f'+{phone}')
        if 'minDate' in parmas:
            minDate = parmas['minDate']
        if 'maxDate' in parmas:
            maxDate = parmas['maxDate']
        if 'appointmentTypeID' in parmas:
            appointmentTypeID = parmas['appointmentTypeID']
        if 'calendarID' in parmas:
            calendarID = parmas['calendarID']
        if 'direction' in parmas:
            direction = parmas['direction']
        url_params = 'max={}&email={}&firstName={}&lastName={}&phone={}&minDate={}' \
                     '&maxDate={}&appointmentTypeID={}&calendarID={}&direction={}'.format(
            max, email, firstName, lastName, phone, minDate,
            maxDate, appointmentTypeID, calendarID, direction
        )
        url = '%s/appointments?%s' % (settings.ACUITY_API_URL, str(url_params))
        res = session.get(url)
        # print(res.json())
        return res.json()

    @staticmethod
    def appointment_detail(appointment_id):
        url = '%s/appointments/%s' % (settings.ACUITY_API_URL, appointment_id)
        res = session.get(url)
        return res.json()

    @staticmethod
    def appointment_update(appointment_id, data):
        url = '%s/appointments/%s' % (settings.ACUITY_API_URL, appointment_id)
        res = session.put(url, data)
        return res.json()

    @staticmethod
    def appointment_types():
        url = '%s/appointment-types' % settings.ACUITY_API_URL
        res = session.get(url)
        return res.json()

    @staticmethod
    def appointment_addons():
        url = '%s/appointment-addons' % settings.ACUITY_API_URL
        res = session.get(url)
        return res.json()
