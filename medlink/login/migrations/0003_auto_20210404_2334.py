# Generated by Django 3.1.7 on 2021-04-04 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20210331_2217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hospitalprofile',
            old_name='base_rofile',
            new_name='base_profile',
        ),
    ]
