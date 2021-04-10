from django_filters import FilterSet, filters
from phonenumber_field.modelfields import PhoneNumberField
from .models import Test, TestType


class TestResultFilterSet(FilterSet):
    first_name = filters.CharFilter(field_name='acuity_appointment__appointment_data__firstName', label='First Name',
                                    lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='acuity_appointment__appointment_data__lastName', label='Last Name',
                                   lookup_expr='icontains')

    email = filters.CharFilter(field_name='acuity_appointment__appointment_data__email', label='Email',
                               lookup_expr='icontains')
    phone = filters.CharFilter(field_name='acuity_appointment__appointment_data__phone', label='Phone',
                               lookup_expr='icontains')
    appointment_id = filters.CharFilter(field_name='acuity_appointment__acuity_appointment_id', label='Appointment ID',
                                        lookup_expr='icontains')
    test_type = filters.ModelChoiceFilter(field_name='test_type', label='Test Type', queryset=TestType.objects.all())

    class Meta:
        model = Test
        fields = ['first_name', 'last_name', 'email', 'phone', 'appointment_id', 'test_type']
        # fields = ['first_name', 'last_name', ]
