# Generated by Django 5.1.1 on 2024-10-04 01:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0007_alter_teamjoinrequestnotification_team_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamjoinrequestnotification',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
