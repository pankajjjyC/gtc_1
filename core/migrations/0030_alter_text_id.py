# Generated by Django 3.2.15 on 2022-10-12 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_rename_app_per_jesse_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
