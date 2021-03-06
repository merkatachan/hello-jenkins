# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 10:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tblCompany',
            fields=[
                ('companyID', models.AutoField(primary_key=True, serialize=False)),
                ('company', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('postalCode', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=32)),
                ('dateAdded', models.DateTimeField()),
            ],
            options={
                'db_table': 'tblCompany',
            },
        ),
        migrations.CreateModel(
            name='tblMine',
            fields=[
                ('mineID', models.AutoField(primary_key=True, serialize=False)),
                ('mine', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('postalCode', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=32)),
                ('dateAdded', models.DateTimeField()),
            ],
            options={
                'db_table': 'tblMine',
            },
        ),
        migrations.CreateModel(
            name='tblUsers',
            fields=[
                ('userID', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('company', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=32)),
                ('jobTitle', models.CharField(max_length=50)),
                ('userRole', models.IntegerField()),
                ('password', models.CharField(max_length=64)),
                ('lastLogin', models.DateTimeField()),
                ('dateAdded', models.DateTimeField()),
                ('companyID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.tblCompany')),
                ('mineID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.tblMine')),
            ],
            options={
                'db_table': 'tblUsers',
            },
        ),
    ]
