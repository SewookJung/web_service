# Generated by Django 2.0.13 on 2020-02-12 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_auto_20200212_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='member_age',
        ),
    ]
