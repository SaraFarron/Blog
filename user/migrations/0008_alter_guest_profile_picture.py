# Generated by Django 4.0.6 on 2022-08-08 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_populate_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='profile_picture',
            field=models.CharField(blank=True, default='/static/images/profile.png', max_length=256, null=True, verbose_name='profile picture'),
        ),
    ]
