# Generated by Django 5.1.1 on 2024-09-18 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_jobseekernotification_application_accepted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseekernotification',
            name='application_accepted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='jobseekernotification',
            name='application_rejected',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
