# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LogAdmin', '0004_auto_20171211_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='project',
        ),
        migrations.AddField(
            model_name='application',
            name='project',
            field=models.ForeignKey(default=1, to='LogAdmin.Project'),
            preserve_default=False,
        ),
    ]
