# Generated by Django 5.1.1 on 2024-10-02 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_alter_teamjobseeker_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamjobseeker',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('member', 'Normal Member')], default='member', max_length=6),
        ),
    ]
