# Generated by Django 4.1.2 on 2022-10-29 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0013_recruiterprofile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruiterprofile',
            name='bio',
        ),
    ]
