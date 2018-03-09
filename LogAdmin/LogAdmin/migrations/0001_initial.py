# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('HID', models.AutoField(serialize=False, primary_key=True)),
                ('hostname', models.CharField(max_length=30)),
                ('ip', models.CharField(max_length=30)),
                ('secret', models.CharField(max_length=30)),
            ],
        ),
    ]
