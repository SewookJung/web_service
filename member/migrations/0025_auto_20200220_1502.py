# Generated by Django 2.0.13 on 2020-02-20 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0024_auto_20200214_1307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='member_id',
            new_name='member_name',
        ),
    ]