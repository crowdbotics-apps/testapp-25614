from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.postgres import fields
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django_json_widget.widgets import JSONEditorWidget

from golab.models import AcuityAppointment
from users.forms import UserChangeForm, UserCreationForm, UserProfileForm
from users.models import UserProfile, LoginOTP, PatientNotification

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name", "phone_number")}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "appointment_ids", "first_name", "last_name", "email", "phone_number",
                    "is_superuser",
                    "is_staff",
                    "is_patient",
                    "date_joined"]
    list_editable = ['is_patient']
    search_fields = ["username", "name", "first_name", "last_name", "phone_number", "date_joined"]

    # filter_horizontal = ['acuityappointment']

    # list_select_related = ['acuityappointment_set']

    def appointment_ids(self, instance):
        # ids = instance.acuityappointment_set.values_list(
        #     'acuity_appointment_id', flat=True,).distinct()
        ids = instance.appointment_ids
        if ids:
            return ids
        return None

    #
    appointment_ids.short_description = 'Appointments'

    def get_queryset(self, request):
        queryset = super(UserAdmin, self).get_queryset(request)
        # queryset = queryset.prefetch_related('acuityappointment_set')
        apps = AcuityAppointment.objects.all()
        queryset = queryset.prefetch_related(
            Prefetch('acuityappointment_set', to_attr='appointment_ids',
                     queryset=apps)
        )
        return queryset


@admin.register(UserProfile)
class UserPofileAdmin(admin.ModelAdmin):
    form = UserProfileForm
    list_display = ['user', 'user__first_name', 'user__last_name', 'date_of_birth', 'contact_number', 'zip_code',
                    'created']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'date_of_birth', 'contact_number',
                     'zip_code', 'created']

    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }

    def user__first_name(self, obj):
        return obj.user.first_name

    def user__last_name(self, obj):
        return obj.user.last_name

    user__first_name.short_description = 'First Name'
    user__first_name.admin_order_field = 'user__first_name'

    user__last_name.short_description = 'Last Name'
    user__last_name.admin_order_field = 'user__last_name'


@admin.register(LoginOTP)
class LoginOTPAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(PatientNotification)
class PatientNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'sms_status', 'email_status', 'created', 'updated']
    # readonly_fields = ['user', 'acuity_appointment']
    raw_id_fields = ['user', 'acuity_appointment']
