# Generated by Django 2.0.13 on 2020-09-14 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0030_remove_member_pw'),
        ('equipment', '0009_auto_20200908_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('operating', 'operating'), ('disposal', 'disposal'), ('return', 'return')], default='operating', max_length=10)),
                ('comments', models.CharField(default='', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('equipment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='equipment.Equipment')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='member.Member')),
            ],
        ),
    ]