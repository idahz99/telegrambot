# Generated by Django 3.2.8 on 2021-12-18 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Pkob', '0009_alter_people_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='people',
            name='Timestamp',
        ),
    ]
