# Generated by Django 4.1.2 on 2022-10-08 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='signup_type',
            field=models.CharField(blank=True, choices=[('manual', 'Manual'), ('google', 'Google'), ('github', 'GitHub'), ('twitter', 'Twitter')], max_length=12, null=True),
        ),
    ]