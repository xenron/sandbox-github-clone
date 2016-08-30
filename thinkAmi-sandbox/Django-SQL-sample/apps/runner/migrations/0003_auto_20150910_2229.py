# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0002_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='CascadeKey',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Deletion',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('cascade_row', models.ForeignKey(to='runner.CascadeKey')),
            ],
        ),
        migrations.CreateModel(
            name='DoNothingKey',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProtectKey',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SetDefaultKey',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SetKey',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SetNullKey',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='deletion',
            name='do_nothing_row',
            field=models.ForeignKey(to='runner.DoNothingKey', on_delete=django.db.models.deletion.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='deletion',
            name='protect_row',
            field=models.ForeignKey(to='runner.ProtectKey', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='deletion',
            name='set_default_row',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_DEFAULT, default=9, to='runner.SetDefaultKey'),
        ),
        migrations.AddField(
            model_name='deletion',
            name='set_key_row',
            field=models.ForeignKey(on_delete=models.SET(11), default=10, to='runner.SetKey'),
        ),
        migrations.AddField(
            model_name='deletion',
            name='set_null_row',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='runner.SetNullKey', null=True),
        ),
    ]
