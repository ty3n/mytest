# Generated by Django 2.2 on 2021-12-03 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localtest', '0009_auto_20211203_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panel',
            name='_fail',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='panel',
            name='_pass',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
