# Generated by Django 3.2.15 on 2022-09-28 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_identification_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='remove_first_col',
            field=models.BooleanField(default=0, max_length=10, null=True),
        ),
    ]
