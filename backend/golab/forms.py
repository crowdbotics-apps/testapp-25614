from django import forms
from .models import *


class AcuityAppointmentCreateForm(forms.ModelForm):
    datetime = forms.DateTimeField(required=True, widget=forms.DateTimeInput(
        attrs={
            'placeholder': 'Datetime',
            'type': 'datetime-local',

        }, format='%Y-%m-%dT%H:%M'))
    appointment_type_id = forms.IntegerField(required=True)
    calendar_id = forms.IntegerField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    certificate = forms.CharField(required=True)
    notes = forms.Textarea()

    class Meta:
        model = AcuityAppointment
        fields = '__all__'
        exclude = ('user', 'acuity_appointment_id',)

    # def clean_datetime(self):
    #     print()
    #     return self.cleaned_data['datetime']
    def clean(self):
        print(self.cleaned_data)
        return self.cleaned_data

    def save(self, commit=True):
        self.instance.user = self.request.user
        return super(AcuityAppointmentCreateForm, self).save(commit=True)
