# Generated by Django 4.1.2 on 2022-10-29 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_remove_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
