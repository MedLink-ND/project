# Generated by Django 3.1.7 on 2021-04-19 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0006_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]