# Generated by Django 3.1.7 on 2021-04-12 00:24

from django.db import migrations
import signup.models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0003_auto_20210404_2125'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', signup.models.UserManager()),
            ],
        ),
    ]