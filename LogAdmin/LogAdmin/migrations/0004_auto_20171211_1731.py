# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LogAdmin', '0003_auto_20171206_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='project',
            field=models.ManyToManyField(related_name='app_project', to='LogAdmin.Project'),
        ),
    ]
