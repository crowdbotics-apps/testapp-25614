from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    # WARNING!
    """
    Some officially supported features of Crowdbotics Dashboard depend on the initial
    state of this User model (Such as the creation of superusers using the CLI
    or password reset in the dashboard). Changing, extending, or modifying this model
    may lead to unexpected bugs and or behaviors in the automated flows provided
    by Crowdbotics. Change it at your own risk.
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)
    phone_number = PhoneNumberField(_('Phone Number'), default=None, null=True, blank=True)
    is_patient = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    # @property
    # def appointment_ids(self):
    #     return self.acuityappointment_set.all().values_list('acuity_appointment_id', flat=True)


class UserProfile(models.Model):
    MALE = "Male"
    FEMALE = "Female"
    GENDER_CHOICES = (
        (MALE, MALE),
        (FEMALE, FEMALE)
    )
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='user_profile')
    date_of_birth = models.DateField(_('Date of Birth'), default=None, null=True, blank=True)
    contact_number = PhoneNumberField(_('Contact Number'), null=True, blank=True)
    zip_code = models.CharField(_('Zip Code'), default=None, max_length=10, null=True, blank=True)
    street_address = models.CharField(_('Street Address'), default=None, max_length=150, null=True, blank=True)
    gender = models.CharField('Select Gender', choices=GENDER_CHOICES, max_length=10, null=True, blank=True)

    acuity_form_data = JSONField(null=True, default=None)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.user.username

    class Meta:
        ordering = ('-created',)
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class LoginOTP(models.Model):
    OTP_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('canceled', 'Canceled'),
    )
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, null=False)
    otp_hash = models.CharField(max_length=256, null=True, default=None)
    is_used = models.BooleanField(default=False)
    # status = models.CharField(choices=OTP_STATUS, max_length=10, default='pending', null=False)
    # email_sid = models.CharField(max_length=256, default=None, null=True)
    # phone_sid = models.CharField(max_length=256, default=None, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):


TWILIO_SMS_STATUS_CHOICES = (
    ('sent', 'Sent'),
    ('delivered', 'Delivered'),
    ('undelivered', 'Undelivered'),
    ('failed', 'Failed')
)


class PatientNotification(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False,
                             related_name='patient_notification_user')
    acuity_appointment = models.ForeignKey('golab.AcuityAppointment', on_delete=models.CASCADE, default=None,
                                           null=True, blank=True)
    message = models.TextField()
    sms_status = models.CharField(choices=TWILIO_SMS_STATUS_CHOICES, max_length=20, default=None, null=True, blank=True)
    # sms_status = models.BooleanField(default=False)
    twilio_sms_sid = models.CharField(max_length=250, default=None, null=True, blank=True)
    email_status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.user

    class Meta:
        ordering = ('-updated',)
        verbose_name = 'Patient Notification'

        verbose_name_plural = 'Patient Notifications'
