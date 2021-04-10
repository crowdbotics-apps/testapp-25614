# Generated by Django 2.2.17 on 2021-01-04 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_patientnotification_acuity_appointment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginotp',
            name='email_sid',
        ),
        migrations.RemoveField(
            model_name='loginotp',
            name='phone_sid',
        ),
        migrations.RemoveField(
            model_name='loginotp',
            name='status',
        ),
        migrations.AddField(
            model_name='loginotp',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='loginotp',
            name='otp_hash',
            field=models.CharField(default=None, max_length=256),
        ),
    ]