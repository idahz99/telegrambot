# Generated by Django 3.2.8 on 2021-12-18 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Pkob', '0008_alter_people_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='Timestamp',
            field=models.DateField(auto_now_add=True),
        ),
    ]