# Generated by Django 4.1.2 on 2022-10-28 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0012_remove_recruiterprofile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruiterprofile',
            name='bio',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
