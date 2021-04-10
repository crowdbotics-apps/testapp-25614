# Generated by Django 2.2.17 on 2020-12-23 16:42

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_merge_20201221_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, default=None, max_length=128, null=True, region=None, verbose_name='Phone Number'),
        ),
    ]
