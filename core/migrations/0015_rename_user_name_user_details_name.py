# Generated by Django 4.0.5 on 2022-07-29 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_user_details'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_details',
            old_name='user_name',
            new_name='name',
        ),
    ]
