# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LogAdmin', '0002_auto_20171206_1004'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('AID', models.AutoField(serialize=False, primary_key=True)),
                ('aname', models.CharField(max_length=30)),
                ('logpath', models.CharField(max_length=50)),
                ('host', models.ForeignKey(to='LogAdmin.Host')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('LID', models.AutoField(serialize=False, primary_key=True)),
                ('lname', models.CharField(max_length=30)),
                ('application', models.ForeignKey(to='LogAdmin.Application')),
            ],
        ),
        migrations.CreateModel(
            name='LogType',
            fields=[
                ('TID', models.AutoField(serialize=False, primary_key=True)),
                ('typename', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('PID', models.AutoField(serialize=False, primary_key=True)),
                ('pname', models.CharField(max_length=30)),
                ('createtime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='person',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.AddField(
            model_name='log',
            name='logtype',
            field=models.ForeignKey(to='LogAdmin.LogType'),
        ),
        migrations.AddField(
            model_name='application',
            name='project',
            field=models.ManyToManyField(to='LogAdmin.Project'),
        ),
    ]
