# Generated by Django 4.2.5 on 2023-12-07 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BRushAPI', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_banner',
            field=models.ImageField(blank=True, null=True, upload_to='banner/'),
        ),
    ]