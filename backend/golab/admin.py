from django.contrib import admin
from django.contrib.auth import get_user_model
import json
from django.utils.safestring import mark_safe

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer

from .models import *
from reports.views import patient_csv_export_view, acuity_appointment_csv_export_view, patient_csv_export_pcr_view
from django import forms

User = get_user_model()


def json_prettify_styles():
    formatter = HtmlFormatter(style='colorful')
    return formatter.get_style_defs()


def json_prettify(json_data):
    formatter = HtmlFormatter(style='colorful')
    json_text = highlight(
        json.dumps(json_data, sort_keys=True, indent=2),
        JsonLexer(),
        formatter
    )
    style = ''

    return mark_safe(style + json_text)


# Register your models here.

@admin.register(AcuityAppointment)
class AcuityAppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'acuity_appointment_id', 'appointment_type', 'created', 'updated']
    search_fields = ['user__username', 'user__email', 'user__phone_number',
                     'user__first_name', 'user__last_name',
                     'acuity_appointment_id', 'created', 'updated', 'appointment_type']
    list_filter = ['appointment_type']
    raw_id_fields = ('user',)

    exclude = ('appointment_data',)
    readonly_fields = ['acuity_appointment_id', 'appointment_data_prettified']
    actions = ['download_csv']
    autocomplete_fields = ['user']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def download_csv(modeladmin, request, queryset):
        return acuity_appointment_csv_export_view(request, queryset)

    download_csv.short_description = "Download CSV Report"

    def appointment_data_prettified(self, obj):
        return json_prettify(obj.appointment_data)


@admin.register(TestType)
class TestTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'type_description', 'created', 'updated']


class CustomTestModelForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomTestModelForm, self).__init__(*args, **kwargs)
        # self.fields['user'].queryset = User.objects.filter(is_patient=True)  # or something else


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    form = CustomTestModelForm
    list_display = ['Test_type', 'appointment_id', 'patient_name', 'collection_date', 'processing_date',
                    'location', 'specimen_type',
                    'test_status', 'results', 'created', 'updated']
    # raw_id_fields = ['acuity_appointment', ]
    autocomplete_fields = ('acuity_appointment',)
    actions = ['download_csv', 'download_csv_pcr']
    search_fields = ['processing_date']
    change_list_template = 'golab/change_test_list.html'

    class Media:
        js = ['/static/js/sb-admin-result-change.js']

    def lookup_allowed(self, lookup, value):
        return True

    def results(self, obj):
        return obj.result

    def patient_name(self, obj):
        if obj.acuity_appointment and obj.acuity_appointment.user:
            first_name = obj.acuity_appointment.appointment_data['firstName']
            last_name = obj.acuity_appointment.appointment_data['lastName']
            return f'{first_name} ' \
                   f'{last_name}'
        return ''

    patient_name.short_description = 'Patient Name'

    def appointment_id(self, instance):
        return '%s' % instance.acuity_appointment.acuity_appointment_id

    appointment_id.short_description = 'Appointment ID'

    def Test_type(self, obj):
        test_types = ''
        for t_type in obj.test_type.all():
            test_types += t_type.type_name + ' '
        return test_types

    def download_csv(modeladmin, request, queryset):
        return patient_csv_export_view(request, queryset)

    download_csv.short_description = "Download CSV Report - POC"

    def download_csv_pcr(modeladmin, request, queryset):
        return patient_csv_export_pcr_view(request, queryset)

    download_csv_pcr.short_description = "Download CSV Report - PCR"


@admin.register(FactSheetUpload)
class FactSheetUploadAdmin(admin.ModelAdmin):
    list_display = ['created', 'sheet', 'updated']

    def has_add_permission(self, request, obj=None):
        count = FactSheetUpload.objects.all().count()
        if count == 0:
            return True
        else:
            return False
