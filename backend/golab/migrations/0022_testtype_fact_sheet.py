# Generated by Django 2.2.17 on 2021-01-21 16:21

from django.db import migrations, models
import golab.models


class Migration(migrations.Migration):

    dependencies = [
        ('golab', '0021_merge_20210114_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='testtype',
            name='fact_sheet',
            field=models.FileField(blank=True, default=None, null=True, upload_to=golab.models.factsheet_directory, verbose_name='Fact sheet'),
        ),
    ]
