# Generated by Django 2.0.13 on 2020-02-28 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0012_auto_20200228_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='cpu',
            field=models.CharField(default='', max_length=100),
        ),
    ]