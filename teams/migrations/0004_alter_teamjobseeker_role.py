# Generated by Django 5.1.1 on 2024-10-02 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_team_specialization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamjobseeker',
            name='role',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
