# Generated by Django 3.2.15 on 2022-12-14 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20221130_2020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='cut_off_thresold',
        ),
    ]
