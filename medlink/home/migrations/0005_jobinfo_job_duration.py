# Generated by Django 3.1.7 on 2021-04-12 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_jobinfo_job_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobinfo',
            name='job_duration',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
