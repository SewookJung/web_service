# Generated by Django 2.0.13 on 2020-10-22 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '__first__'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Client'),
        ),
        migrations.AddField(
            model_name='project',
            name='mnfacture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Mnfacture'),
        ),
        migrations.AddField(
            model_name='project',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Product'),
        ),
    ]
