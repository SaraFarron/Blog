# Generated by Django 4.0.4 on 2022-05-16 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0008_alter_comment_owner_pfp_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='owner_pfp_url',
            field=models.CharField(blank=True, max_length=256, verbose_name='owner pfp url'),
        ),
    ]
