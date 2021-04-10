from allauth.account.adapter import get_adapter
from allauth.account import forms as allauth_account_forms
from allauth.account import app_settings
from allauth.account.utils import get_next_redirect_url, perform_login
from django.conf import settings
from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from django import forms as django_forms
from users.models import UserProfile

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    phone_number = PhoneNumberField(required=False)

    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    phone_number = PhoneNumberField(required=False)
    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class UserProfileForm(ModelForm):
    contact_number = PhoneNumberField(required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'


class CustomAdminLoginForm(allauth_account_forms.LoginForm):

    def clean(self):
        super(CustomAdminLoginForm, self).clean()
        # if self.user is not None and not self.user.is_patient:
        #     raise django_forms.ValidationError(_('You are not registered as Patient'))
        # print(self.cleaned_data)
        if not (self.user.is_superuser or self.user.is_staff):
            print('not staff')
            raise django_forms.ValidationError(_('You are not authorized to perform this action'))
        return self.cleaned_data

    def login(self, request, redirect_url=None):
        new_redirect_url = redirect_url
        # if self.user.is_superuser or self.user.is_staff:
        #     new_redirect_url = '/admin/dashboard/'
        ret = perform_login(request, self.user,
                            email_verification=app_settings.EMAIL_VERIFICATION,
                            redirect_url=new_redirect_url)
        remember = app_settings.SESSION_REMEMBER
        if remember is None:
            remember = self.cleaned_data['remember']
        if remember:
            request.session.set_expiry(app_settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)
        return ret


class PatientLoginForm(allauth_account_forms.LoginForm):

    def clean(self):
        super(PatientLoginForm, self).clean()
        # if self.user is not None and not self.user.is_patient:
        #     raise django_forms.ValidationError(_('You are not registered as Patient'))
        return self.cleaned_data

    def login(self, request, redirect_url=None):
        new_redirect_url = redirect_url
        if self.user.is_superuser or self.user.is_staff:
            new_redirect_url = '/admin/dashboard/'
        ret = perform_login(request, self.user,
                            email_verification=app_settings.EMAIL_VERIFICATION,
                            redirect_url=new_redirect_url)
        remember = app_settings.SESSION_REMEMBER
        if remember is None:
            remember = self.cleaned_data['remember']
        if remember:
            request.session.set_expiry(app_settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)
        return ret


class PatientRegisterForm(forms.UserCreationForm):
    phone_number = PhoneNumberField(required=False)
    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_patient = True
        if commit:
            user.save()
        return user
