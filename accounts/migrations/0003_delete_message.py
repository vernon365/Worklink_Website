# Generated by Django 5.1.1 on 2024-10-04 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_message'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
