# Generated by Django 2.2.17 on 2020-12-20 09:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('golab', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=255, verbose_name='Test Name')),
                ('type_description', models.TextField(blank=True, null=True, verbose_name='Test Description')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Test Type',
                'verbose_name_plural': 'Test Types',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_date', models.DateField(blank=True, null=True, verbose_name='Collection Date')),
                ('processing_date', models.DateField(blank=True, null=True, verbose_name='Processing Date')),
                ('location', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Location')),
                ('specimen_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Specimen Type')),
                ('iterpretation', models.TextField(blank=True, null=True, verbose_name='Interpretation')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('test_type', models.ManyToManyField(to='golab.TestType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Test',
                'verbose_name_plural': 'Test',
                'ordering': ('-created',),
            },
        ),
    ]
