# Generated by Django 3.1.7 on 2021-03-31 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitalprofile',
            name='has_available_job',
        ),
        migrations.AddField(
            model_name='hospitalprofile',
            name='hospital_location_city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hospitalprofile',
            name='hospital_location_state',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hospitalprofile',
            name='hospital_location_zipcode',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hospitalprofile',
            name='looking_for_worker',
            field=models.BooleanField(default=True),
        ),
    ]