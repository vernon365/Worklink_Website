# Generated by Django 5.1.1 on 2024-09-18 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
        ('jobpostings', '0004_alter_jobposting_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='job_posting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobpostings.jobposting'),
        ),
    ]
