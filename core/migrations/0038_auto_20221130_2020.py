# Generated by Django 3.2.15 on 2022-11-30 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_detection_temp_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detection_temp_values',
            name='ml_perf',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='detection_temp_values',
            name='ml_train',
            field=models.IntegerField(null=True),
        ),
    ]
