from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.urls import reverse


class PatientLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous and not request.user.is_authenticated and not request.user.is_patient:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    # def handle_no_permission(self):
    #     if self.raise_exception or self.request.user.is_authenticated:
    #         raise PermissionDenied(self.get_permission_denied_message())
    #     return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def get_login_url(self):
        return reverse('golab:patient_login')
