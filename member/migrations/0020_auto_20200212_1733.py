# -*- coding: utf-8 -*-z
# Generated by Django 2.0.13 on 2020-02-12 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0019_member_member_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_status',
            field=models.CharField(choices=[('Active', 'Active'), ('Passive', 'Passive')], default='Active', max_length=10),
        ),
    ]
