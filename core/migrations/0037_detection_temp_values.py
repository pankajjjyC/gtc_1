# Generated by Django 3.2.15 on 2022-11-25 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_inject_anamolies'),
    ]

    operations = [
        migrations.CreateModel(
            name='detection_temp_values',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('ml_train', models.CharField(default=0, max_length=60, null=True)),
                ('ml_perf', models.CharField(default=0, max_length=60, null=True)),
            ],
        ),
    ]