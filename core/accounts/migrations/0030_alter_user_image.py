# Generated by Django 4.1.2 on 2022-12-02 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_alter_company_image_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='bike.jpeg', null=True, upload_to='user'),
        ),
    ]
