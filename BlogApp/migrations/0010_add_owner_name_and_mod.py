# Generated by Django 4.0.4 on 2022-05-16 09:10

from django.db import migrations, models


def add_owner(apps, schema_editor):
    MyModel = apps.get_model('BlogApp', 'Comment')
    for row in MyModel.objects.all():
        row.owner_name = row.user.name
        row.owner_is_moderator = row.user.is_moderator
        row.save(update_fields=['owner_name', 'owner_is_moderator'])


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0009_alter_comment_owner_pfp_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='owner_name',
            field=models.CharField(blank=True, max_length=128, verbose_name='owner name'),
        ),
        migrations.AddField(
            model_name='comment',
            name='owner_is_moderator',
            field=models.BooleanField(default=False, verbose_name='is owner a mod'),
        ),
        migrations.RunPython(add_owner, reverse_code=migrations.RunPython.noop),
    ]
