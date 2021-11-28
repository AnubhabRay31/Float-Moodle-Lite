# Generated by Django 3.2.8 on 2021-10-18 06:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follos', models.IntegerField(default=0)),
                ('follo_dict', models.JSONField(default=list)),
                ('repo_dict', models.JSONField(default=list)),
                ('updatenowtime', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('numberofstars', models.IntegerField(default=0)),
                ('owner', models.CharField(default='', max_length=100)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moodle.profile')),
            ],
        ),
    ]
