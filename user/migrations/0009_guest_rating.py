# Generated by Django 4.0.1 on 2022-01-23 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_guest_email_alter_guest_is_banned_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='rating'),
        ),
    ]