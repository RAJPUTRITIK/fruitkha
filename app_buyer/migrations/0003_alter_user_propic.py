# Generated by Django 4.2.3 on 2023-07-14 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_buyer', '0002_user_propic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='propic',
            field=models.FileField(default='anonymous.jpg', upload_to='app_buyer/'),
        ),
    ]
