# Generated by Django 3.0.3 on 2020-03-31 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0005_auto_20200330_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentattachment',
            name='check_code',
            field=models.CharField(default='', max_length=128),
        ),
    ]