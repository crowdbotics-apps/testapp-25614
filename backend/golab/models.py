import os

from django.contrib.postgres.fields import JSONField
from django.db import models
# from django.db.models.enums import Choices
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class AcuityAppointment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False)
    acuity_appointment_id = models.BigIntegerField(_('Acuity Appointment ID'), unique=True, default=None, null=False)
    first_name = models.CharField(_('First Name'), null=True, blank=True, max_length=255)
    last_name = models.CharField(_('Last Name'), null=True, blank=True, max_length=255)
    appointment_data = JSONField(null=True, default=dict, blank=True)
    send_sms_notification = models.BooleanField(default=True)
    appointment_type = models.CharField('Appointment Type', null=True, blank=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.acuity_appointment_id

    def __unicode__(self):
        return '%s' % self.pk

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Acuity Appointment'
        verbose_name_plural = 'Acuity Appointments'


def factsheet_directory(instance, filename):
    return os.path.join('factsheets/test_type_%s' % instance.id, filename)


class TestType(models.Model):
    type_name = models.CharField('Test Name', null=False, max_length=255)
    type_description = models.TextField('Test Description', null=True, blank=True)

    fact_sheet = models.FileField('Fact sheet', default=None, upload_to=factsheet_directory, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return "{} - {}".format(self.type_name, self.type_description, self.created, self.updated)

    def __str__(self):
        return self.type_name

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Test Type'
        verbose_name_plural = 'Test Types'


Test_Status = (
    ('check_in', 'Checked In'),
    ('collected', 'Sample collected - swab has been performed'),
    ('processing', 'Sample Processing'),
    ('ready', 'Results ready')
)
Results = (
    ('detected', 'DETECTED'),
    ('not_detected', 'NOT DETECTED')
)

Specimen_types = (
    ('nasopharyngeal_swab', 'Nasopharyngeal Swab'),
    ('nasal_swab', 'Nasal Swab'),
    ('throat_swab', 'Throat Swab')
)


class Test(models.Model):
    acuity_appointment = models.OneToOneField(AcuityAppointment, on_delete=models.CASCADE, null=True, blank=True,
                                              related_name='actuity_appointment_test')
    collection_date = models.DateField('Collection Date', null=True, blank=True)
    processing_date = models.DateField('Processing Date', null=True, blank=True)
    location = models.CharField('Location', null=True, blank=True, max_length=1000)
    specimen_type = models.CharField('Specimen Type', choices=Specimen_types, default=None,
                                     null=True, blank=True, max_length=255)
    test_type = models.ManyToManyField('golab.TestType')
    result = models.CharField('Results', choices=Results, default=None, null=True, blank=True, max_length=15)
    iterpretation = models.TextField('Interpretation', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    test_status = models.CharField('Test Status', choices=Test_Status, max_length=50, null=True, blank=True)
    processed_date = models.DateTimeField(auto_now=True, null=True, blank=True, )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Test Result'
        verbose_name_plural = 'Test Results'

    def __str__(self):
        user = self.acuity_appointment.user if self.acuity_appointment else None
        try:
            return "{} - {}".format(user, self.collection_date, self.processing_date,
                                    self.location, self.specimen_type,
                                    self.test_type, self.iterpretation, self.created, self.updated)
        except Exception:
            return "{} - {}".format(user, self.collection_date)


class FactSheetUpload(models.Model):
    sheet = models.FileField("Select File", upload_to="fact_sheets", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Fact Sheet Upload'
        verbose_name_plural = 'Fact Sheet Upload'

    def __str__(self):
        return "{}".format(self.sheet.name)
