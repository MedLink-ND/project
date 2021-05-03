# Generated by Django 3.1.7 on 2021-05-03 00:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPreference',
            fields=[
                ('job_type', models.CharField(max_length=255, null=True)),
                ('home_location_zipcode', models.IntegerField(null=True)),
                ('home_location_lat', models.FloatField(null=True)),
                ('home_location_lng', models.FloatField(null=True)),
                ('job_location_radius', models.CharField(max_length=255, null=True)),
                ('hospital_type', models.CharField(max_length=255, null=True)),
                ('job_on_call', models.CharField(max_length=255, null=True)),
                ('job_start_time', models.DateTimeField(null=True)),
                ('job_end_time', models.DateTimeField(null=True)),
                ('locum_shift_day', models.CharField(max_length=255, null=True)),
                ('locum_shift_hour', models.CharField(max_length=255, null=True)),
                ('job_experience', models.CharField(max_length=255, null=True)),
                ('job_supervision', models.CharField(max_length=255, null=True)),
                ('job_payment', models.CharField(max_length=255, null=True)),
                ('base_profile', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='JobInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=255, null=True)),
                ('job_type', models.CharField(max_length=255, null=True)),
                ('job_location_zipcode', models.IntegerField(null=True)),
                ('job_location_hospital', models.CharField(max_length=255, null=True)),
                ('hospital_type', models.CharField(max_length=255, null=True)),
                ('job_on_call', models.CharField(max_length=255, null=True)),
                ('job_start_time', models.DateTimeField(null=True)),
                ('job_end_time', models.DateTimeField(null=True)),
                ('locum_shift_day', models.CharField(max_length=255, null=True)),
                ('locum_shift_hour', models.CharField(max_length=255, null=True)),
                ('job_experience', models.CharField(max_length=255, null=True)),
                ('job_supervision', models.CharField(max_length=255, null=True)),
                ('job_payment', models.CharField(max_length=255, null=True)),
                ('job_vacation', models.CharField(max_length=255, null=True)),
                ('education_money', models.CharField(max_length=255, null=True)),
                ('base_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobApplicants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255, null=True)),
                ('job_status', models.CharField(default='', max_length=255, null=True)),
                ('job_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.jobinfo')),
            ],
        ),
    ]
