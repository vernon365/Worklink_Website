# Generated by Django 5.1.1 on 2025-04-01 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0013_jobpostingnotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobpostingnotification',
            name='applicant',
        ),
    ]
