# Generated by Django 2.2 on 2021-12-03 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localtest', '0007_auto_20211116_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panel',
            name='_fail',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='panel',
            name='_pass',
            field=models.IntegerField(default=0),
        ),
    ]
