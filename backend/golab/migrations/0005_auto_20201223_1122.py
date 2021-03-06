# Generated by Django 2.2.17 on 2020-12-23 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golab', '0004_factsheetupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='test_status',
            field=models.CharField(blank=True, choices=[('check_in', 'Check In'), ('sample_collected', 'Sample collected - swab has been performed'), ('sample_processing', 'Sample Processing'), ('results_ready', 'Results ready')], max_length=30, null=True, verbose_name='Test Status'),
        ),
        migrations.AlterField(
            model_name='test',
            name='result',
            field=models.CharField(blank=True, choices=[('detected', 'DETECTED'), ('not_detected', 'NOT DETECTED')], max_length=15, null=True, verbose_name='Results'),
        ),
    ]
