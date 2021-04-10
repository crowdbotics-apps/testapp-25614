from rest_framework.permissions import BasePermission


class StaffPermissionForAppointment(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('golab.change_acuityappointment')
