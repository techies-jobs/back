# Generated by Django 4.1.2 on 2022-10-08 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_signup_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_type',
            field=models.CharField(blank=True, choices=[('manual', 'Manual'), ('google', 'Google'), ('github', 'GitHub'), ('twitter', 'Twitter')], max_length=12, null=True),
        ),
    ]
