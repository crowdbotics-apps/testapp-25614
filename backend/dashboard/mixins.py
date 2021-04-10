from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import reverse

# staff_views
staff_urls_only = []


class StaffViewsPermissionOnly(PermissionRequiredMixin):
    def has_permission(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return True

        return False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not (request.user.is_superuser or request.user.is_staff):
            return redirect(reverse('golab:patient_dashboard'))
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AdminOnlyViewPermissionMixin(PermissionRequiredMixin):

    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """
        if self.permission_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attribute. Define {0}.permission_required, or override '
                '{0}.get_permission_required().'.format(self.__class__.__name__)
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def has_permission(self):
        # perms = self.get_permission_required()
        return self.request.user.is_superuser
        # return (self.request.user.is_superuser or self.request.user.is_staff)

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and not (request.user.is_superuser or request.user.is_staff):
            return redirect(reverse('golab:patient_dashboard'))
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
