# Generated by Django 2.0.13 on 2020-10-16 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0003_auto_20201016_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='product_model',
        ),
    ]
