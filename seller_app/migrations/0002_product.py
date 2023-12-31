# Generated by Django 4.2.3 on 2023-07-15 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('p_quantity', models.IntegerField(default=0)),
                ('desc', models.CharField(max_length=500)),
                ('pimage', models.FileField(default='anonymous1.jpg', upload_to='seller_profile')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller_app.seller_user')),
            ],
        ),
    ]
