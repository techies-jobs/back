# Generated by Django 4.1.2 on 2022-12-02 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0015_recruiterprofile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruiterprofile',
            name='image',
        ),
    ]
