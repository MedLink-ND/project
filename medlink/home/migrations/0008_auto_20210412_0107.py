# Generated by Django 3.1.7 on 2021-04-12 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_jobinfo_job_start_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobinfo',
            name='job_end_month',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='jobinfo',
            name='job_end_year',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
