from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def patient_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    redirect_login_url = '/golab/patient/login/'
    if login_url is not None:
        redirect_login_url = login_url
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_patient,
        login_url=redirect_login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
