# Generated by Django 2.2.17 on 2021-01-14 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20210107_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientnotification',
            name='twilio_sms_sid',
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
    ]
