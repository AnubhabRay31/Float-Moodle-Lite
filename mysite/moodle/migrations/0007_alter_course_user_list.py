# Generated by Django 3.2.8 on 2021-10-18 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0006_profile_user_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='user_list',
            field=models.JSONField(default=dict),
        ),
    ]
