# Generated by Django 2.2.17 on 2020-12-23 15:07

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('golab', '0004_factsheetupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='acuityappointment',
            name='appointment_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
    ]
