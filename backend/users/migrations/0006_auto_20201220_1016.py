# Generated by Django 2.2.17 on 2020-12-20 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20201220_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginotp',
            name='is_used',
        ),
        migrations.RemoveField(
            model_name='loginotp',
            name='otp_hash',
        ),
    ]
