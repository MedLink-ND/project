# Generated by Django 3.2 on 2021-05-10 01:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0006_auto_20210509_0527'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=5, null=True)),
                ('education', models.CharField(max_length=255, null=True)),
                ('provider_type', models.CharField(max_length=255, null=True)),
                ('peer_references', models.CharField(max_length=255, null=True)),
                ('cpr_certifications', models.CharField(max_length=255, null=True)),
                ('base_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
