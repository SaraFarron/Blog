# Generated by Django 4.0.6 on 2022-08-07 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_guest_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='profile_picture',
            field=models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='profile picture'),
        ),
    ]
