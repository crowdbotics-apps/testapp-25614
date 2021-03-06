# Generated by Django 2.2.17 on 2021-01-14 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_remove_patientnotification_sms_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientnotification',
            name='sms_status',
            field=models.CharField(blank=True, choices=[('sent', 'Sent'), ('delivered', 'Delivered'), ('undelivered', 'Undelivered'), ('failed', 'Failed')], default=None, max_length=20, null=True),
        ),
    ]
