# Generated by Django 5.1.1 on 2024-10-04 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobpostings', '0006_alter_interview_employer_alter_interview_job_seeker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobposting',
            name='remote',
        ),
        migrations.AddField(
            model_name='jobposting',
            name='industry',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
