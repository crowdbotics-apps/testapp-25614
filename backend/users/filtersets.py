from django_filters import FilterSet, filters
from phonenumber_field.modelfields import PhoneNumberField
from .models import PatientNotification


class PatientNotificationFilterSet(FilterSet):
    first_name = filters.CharFilter(field_name='user__first_name', label='First Name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='user__last_name', label='Last Name', lookup_expr='icontains')
    email = filters.CharFilter(field_name='user__email', label='Email', lookup_expr='icontains')
    phone = filters.CharFilter(field_name='user__phone_number', label='Phone', lookup_expr='icontains')
    appointment_id = filters.CharFilter(field_name='acuity_appointment__acuity_appointment_id', label='Appointment ID',
                                        lookup_expr='icontains')

    class Meta:
        model = PatientNotification
        fields = ['first_name', 'last_name', 'email', 'phone', 'appointment_id']

        # filter_overrides = {
        #     PhoneNumberField: {
        #         'filter_class': filters.CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #         },
        #     },
        # }
