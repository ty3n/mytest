# Generated by Django 2.2 on 2021-12-03 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localtest', '0010_auto_20211203_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='panel',
            name='_fail',
        ),
        migrations.RemoveField(
            model_name='panel',
            name='_pass',
        ),
    ]
