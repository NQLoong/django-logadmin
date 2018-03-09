# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LogAdmin', '0006_auto_20171219_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='apptype',
            field=models.ForeignKey(default=1, to='LogAdmin.AppType'),
            preserve_default=False,
        ),
    ]
