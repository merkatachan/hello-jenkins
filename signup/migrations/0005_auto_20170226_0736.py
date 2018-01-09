# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 12:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0004_auto_20170218_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblusers',
            name='company',
        ),
        migrations.AlterField(
            model_name='tblusers',
            name='companyID',
            field=models.ForeignKey(db_column='companyID', on_delete=django.db.models.deletion.CASCADE, to='signup.tblCompany'),
        ),
        migrations.AlterField(
            model_name='tblusers',
            name='mineID',
            field=models.ForeignKey(db_column='mineID', on_delete=django.db.models.deletion.CASCADE, to='signup.tblMine'),
        ),
    ]