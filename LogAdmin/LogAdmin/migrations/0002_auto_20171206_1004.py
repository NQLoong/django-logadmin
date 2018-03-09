# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LogAdmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=10, verbose_name=b'\xe4\xb9\xa6\xe7\xb1\x8d\xe5\x90\x8d\xe7\xa7\xb0')),
                ('pubtime', models.DateField(verbose_name=b'\xe5\x87\xba\xe7\x89\x88\xe6\x97\xb6\xe9\x97\xb4')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85\xe5\xa7\x93\xe5\x90\x8d')),
                ('age', models.IntegerField(verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85\xe5\xb9\xb4\xe9\xbe\x84')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='person',
            field=models.ForeignKey(related_name='person_book', to='LogAdmin.Person'),
        ),
    ]
