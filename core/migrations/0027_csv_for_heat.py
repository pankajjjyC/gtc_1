# Generated by Django 3.2.15 on 2022-10-11 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_csv_score_downld'),
    ]

    operations = [
        migrations.CreateModel(
            name='Csv_for_heat',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('csv', models.FileField(upload_to='')),
            ],
        ),
    ]