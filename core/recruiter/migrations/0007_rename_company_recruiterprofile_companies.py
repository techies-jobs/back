# Generated by Django 4.1.2 on 2022-10-23 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0006_recruiterprofile_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recruiterprofile',
            old_name='company',
            new_name='companies',
        ),
    ]
