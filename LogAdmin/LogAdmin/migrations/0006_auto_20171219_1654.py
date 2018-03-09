# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LogAdmin', '0005_auto_20171212_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppType',
            fields=[
                ('TID', models.AutoField(serialize=False, primary_key=True)),
                ('tname', models.CharField(unique=True, max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='log',
            name='application',
        ),
        migrations.RemoveField(
            model_name='log',
            name='logtype',
        ),
        migrations.AlterField(
            model_name='application',
            name='aname',
            field=models.CharField(unique=True, max_length=30),
        ),
        migrations.DeleteModel(
            name='Log',
        ),
        migrations.DeleteModel(
            name='LogType',
        ),
    ]
