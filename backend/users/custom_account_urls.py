from django.urls import path
from users.views import (
    PatientSignup, PatientLogout, CustomUserLogin, AdminAccountForgotPassword, AdminAccountProfileInfoUpdate,
    AdminAccountProfileUpdate, logged_account_profile
)

urlpatterns = [
    path("login/", CustomUserLogin.as_view(), name='account_login'),
    path('logout/', PatientLogout.as_view(), name="account_logout"),
    path('signup/', PatientSignup.as_view(), name="account_signup"),
    path('forgot-password/', AdminAccountForgotPassword.as_view(), name="account_forgot_password"),
    path('profile/', logged_account_profile, name="logged_account_profile"),
    path('profile/info/', AdminAccountProfileInfoUpdate.as_view(), name="logged_account_profile_info"),
    path('profile/update/', AdminAccountProfileUpdate.as_view(), name="account_update"),
]
