# Generated by Django 4.1.2 on 2022-10-29 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('techie', '0011_techieprofile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='techieprofile',
            name='bio',
        ),
    ]