# Generated by Django 5.1.1 on 2024-09-18 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobpostings', '0003_savedjob'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobposting',
            options={'ordering': ['-posted_date']},
        ),
    ]
