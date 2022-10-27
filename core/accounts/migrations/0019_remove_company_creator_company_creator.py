# Generated by Django 4.1.2 on 2022-10-27 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0011_alter_recruiterprofile_user'),
        ('accounts', '0018_company_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='creator',
        ),
        migrations.AddField(
            model_name='company',
            name='creator',
            field=models.ManyToManyField(blank=True, to='recruiter.recruiterprofile'),
        ),
    ]
