# Generated by Django 4.1.2 on 2022-10-28 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('techie', '0009_techieprofile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='techieprofile',
            name='image',
        ),
    ]
