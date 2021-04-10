from allauth.account.adapter import get_adapter
from allauth.account.utils import passthrough_next_redirect_url, get_next_redirect_url
from allauth.account.views import _ajax_response, sensitive_post_parameters_m
from allauth.exceptions import ImmediateHttpResponse
from allauth.utils import get_request_param
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password, PBKDF2PasswordHasher
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView, TemplateView
from allauth.account import views as allauth_account_views

from golab.decorators import patient_login_required
from users.forms import PatientLoginForm, PatientRegisterForm, CustomAdminLoginForm
from users.models import UserProfile, LoginOTP

from home.twilio import (
    twilio_send_verification_code, twilio_check_verification, twilio_verification_status_update
)

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class CustomUserLogin(allauth_account_views.LoginView):
    form_class = CustomAdminLoginForm
    template_name = 'dashboard/account/login.html'
    success_url = '/admin/dashboard/'

    def get_form_kwargs(self):
        kwargs = super(CustomUserLogin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        ret = super(CustomUserLogin, self).get_context_data(**kwargs)
        signup_url = passthrough_next_redirect_url(self.request,
                                                   reverse("account_signup"),
                                                   self.redirect_field_name)
        redirect_field_value = get_request_param(self.request,
                                                 self.redirect_field_name)

        # if self.request.user.is_superuser or self.request.user.is_staff:
        #     redirect_field_value = '/admin/dashboard/'
        #
        # elif self.request.user.is_patient:
        #     redirect_field_value = self.success_url

        # if redirect_field_value is None:
        #     redirect_field_value = self.success_url

        site = get_current_site(self.request)

        ret.update({"signup_url": signup_url,
                    "site": site,
                    "redirect_field_name": self.redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret


class PatientLogin(allauth_account_views.LoginView):
    form_class = PatientLoginForm
    template_name = 'golab/patient/account/login.html'
    success_url = '/golab/patient/dashboard/'

    def get_form_kwargs(self):
        kwargs = super(PatientLogin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        ret = super(PatientLogin, self).get_context_data(**kwargs)
        signup_url = passthrough_next_redirect_url(self.request,
                                                   reverse("account_signup"),
                                                   self.redirect_field_name)
        redirect_field_value = get_request_param(self.request,
                                                 self.redirect_field_name)
        if redirect_field_value is None:
            redirect_field_value = self.success_url
        site = get_current_site(self.request)

        ret.update({"signup_url": signup_url,
                    "site": site,
                    "redirect_field_name": self.redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret


class PatientOtpLogin(TemplateView):
    template_name = 'golab/patient/account/otp_login.html'

    def get_context_data(self, **kwargs):
        context = super(PatientOtpLogin, self).get_context_data(**kwargs)
        context['title'] = 'Patient Login'
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_patient:
                return redirect(reverse('golab:patient_dashboard'))
            elif request.user.is_staff or request.user.is_superuser:
                return redirect(reverse('dashboard:dashboard_index'))
        return super(PatientOtpLogin, self).get(request, *args, **kwargs)


# def patient_custom_login(request):
#     if not request.user.is_authenticated:
#         if request.method == ""

def verify_otp_and_login(request):
    if request.method == 'POST':
        otp_number = request.POST.get('otp')
        email = request.POST.get('email').lower()
        user = User.objects.get(email=email)
        try:

            otp_object = LoginOTP.objects.get(user=user, is_used=False)
            print('otp found: ', otp_object.is_used)
        except LoginOTP.DoesNotExist:
            return JsonResponse(status=404, data={
                "message": "Verification failed"
            })
        # is_verified = False
        if otp_object:
            try:
                otp_hash = make_password(otp_number, salt=settings.SECRET_KEY)
                is_verified = (otp_hash == otp_object.otp_hash)
            except:
                is_verified = False
            # try:
            #     print('trying email')
            #     # otp_object.email_sid
            #     is_verified = twilio_check_verification(
            #         otp_object, otp_number, otp_object.email_sid)
            # except:
            #     print('email failed')
            #     print('trying phone')
            #     # otp_object.phone_sid
            #     is_verified = twilio_check_verification(
            #         otp_object, otp_number, otp_object.phone_sid)
            # else:
            #     is_verified = False

            if is_verified:
                # try:
                #     twilio_verification_status_update(otp_object.email_sid, 'approved')
                # except:
                #     pass
                # try:
                #     twilio_verification_status_update(otp_object.phone_sid, 'approved')
                # except:
                #     pass
                try:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    otp_object.delete()
                    if user.is_patient:
                        return redirect(reverse('golab:patient_dashboard'))
                    return redirect(reverse('golab:patient_dashboard'))
                except:
                    return JsonResponse(status=404, data={
                        "message": "Invalid verification code"
                    })
            return JsonResponse(status=404, data={
                "message": "Verification failed. Try after sometime"
            })
        return JsonResponse(status=404, data={
            "message": "Verification failed"
        })
    return JsonResponse(status=404, data={
        "message": "Verification failed"
    })


class PatientSignup(allauth_account_views.SignupView):
    template_name = 'golab/patient/account/signup.html'
    form_class = PatientRegisterForm

    def get_context_data(self, **kwargs):
        ret = super(PatientSignup, self).get_context_data(**kwargs)
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("golab:patient_login"),
                                                  self.redirect_field_name)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = get_request_param(self.request,
                                                 redirect_field_name)
        if not redirect_field_value:
            redirect_field_value = login_url
        ret.update({"login_url": login_url,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret


class PatientLogout(allauth_account_views.LogoutView):
    def post(self, *args, **kwargs):
        url = self.get_redirect_url()
        if self.request.user.is_authenticated:
            self.logout()
        response = redirect(url)
        return _ajax_response(self.request, response)

    def get_redirect_url(self):
        if self.request.user.is_patient:
            return reverse('golab:patient_login')
        else:
            return reverse('account_login')


@patient_login_required
def logged_patient_profile(request):
    return render(request, 'golab/patient/account/profile.html')


class PatientProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'name', ]
    template_name = 'golab/patient/account/update.html'
    success_message = 'Profile successfull updated.'

    def get_success_url(self):
        return reverse("golab:patient_account_update")

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


class PatientProfileInfoUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    fields = ['date_of_birth', 'contact_number', 'zip_code', 'street_address', 'gender']
    template_name = 'golab/patient/account/profile_info.html'
    success_message = 'Profile info successfull updated.'

    def get_success_url(self):
        return reverse("golab:logged_patient_profile_info")

    def get_object(self):
        try:
            user_info = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            user_info = UserProfile.objects.create(user=self.request.user)
        return user_info


class PatientAccountForgotPassword(allauth_account_views.PasswordResetView):
    template_name = 'golab/patient/account/forgot_password.html'


@login_required()
def logged_account_profile(request):
    return render(request, 'users/profile.html')


class AdminAccountProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'name', ]
    template_name = 'users/update.html'
    success_message = 'Profile successfull updated.'

    def get_success_url(self):
        return reverse("account_update")

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


class AdminAccountProfileInfoUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    fields = ['date_of_birth', 'contact_number', 'zip_code', 'street_address']
    template_name = 'users/profile_info.html'
    success_message = 'Profile info successfull updated.'

    def get_success_url(self):
        return reverse("logged_account_profile_info")

    def get_object(self):
        try:
            user_info = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            user_info = UserProfile.objects.create(user=self.request.user)
        return user_info


class AdminAccountForgotPassword(allauth_account_views.PasswordResetView):
    template_name = 'users/forgot_password.html'
