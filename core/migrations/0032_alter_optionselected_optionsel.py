# Generated by Django 3.2.15 on 2022-10-21 12:38

from django.db import migrations, models
import sqlalchemy.sql.expression


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_optionselected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionselected',
            name='optionsel',
            field=models.IntegerField(null=sqlalchemy.sql.expression.true),
        ),
    ]
