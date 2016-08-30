# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('registered_users', models.PositiveIntegerField()),
                ('hoge', models.CharField(max_length=100, default='fuga')),
            ],
            options={
                'db_table': 'store',
            },
        ),
    ]
