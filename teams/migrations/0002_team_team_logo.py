# Generated by Django 5.1.1 on 2024-10-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_logo',
            field=models.ImageField(blank=True, null=True, upload_to='team_logos/'),
        ),
    ]
