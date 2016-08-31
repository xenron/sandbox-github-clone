# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-04 13:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=15, unique=True)),
                ('description', models.CharField(max_length=100)),
                ('registration_date', models.DateField()),
                ('active', models.BooleanField()),
                ('open_ended', models.BooleanField()),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FundScheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FundVolumeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_unit_holders', models.FloatField(blank=True, null=True, verbose_name='No. Unit holders')),
                ('tt_total_net_assets_under_management', models.FloatField(blank=True, null=True)),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Fund')),
            ],
        ),
        migrations.CreateModel(
            name='Issuer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('symbol', models.CharField(max_length=5)),
                ('active', models.BooleanField()),
                ('address_1', models.CharField(blank=True, max_length=100)),
                ('address_2', models.CharField(blank=True, max_length=100)),
                ('is_local_entity', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Monthly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateix', models.DateField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='fundvolumedata',
            name='period_ending',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Monthly', verbose_name='Period'),
        ),
        migrations.AddField(
            model_name='fund',
            name='fund_scheme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.FundScheme'),
        ),
        migrations.AddField(
            model_name='fund',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Issuer'),
        ),
    ]
