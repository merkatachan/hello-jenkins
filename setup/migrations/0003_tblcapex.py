# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0002_auto_20170226_0819'),
    ]

    operations = [
        migrations.CreateModel(
            name='tblCAPEX',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('preStrip', models.DecimalField(decimal_places=2, max_digits=20)),
                ('mineEquipInitial', models.DecimalField(decimal_places=2, max_digits=20)),
                ('mineEquipSustain', models.DecimalField(decimal_places=2, max_digits=20)),
                ('infraDirectCost', models.DecimalField(decimal_places=2, max_digits=20)),
                ('infraIndirectCost', models.DecimalField(decimal_places=2, max_digits=20)),
                ('contingency', models.DecimalField(decimal_places=2, max_digits=20)),
                ('railcars', models.DecimalField(decimal_places=2, max_digits=20)),
                ('otherMobEquip', models.DecimalField(decimal_places=2, max_digits=20)),
                ('closureRehabAssure', models.DecimalField(decimal_places=2, max_digits=20)),
                ('depoProvisionPay', models.DecimalField(decimal_places=2, max_digits=20)),
                ('workCapCurrentProd', models.DecimalField(decimal_places=2, max_digits=20)),
                ('workCapCostsLG', models.DecimalField(decimal_places=2, max_digits=20)),
                ('EPCM', models.DecimalField(decimal_places=2, max_digits=20)),
                ('ownerCost', models.DecimalField(decimal_places=2, max_digits=20)),
                ('dateAdded', models.DateTimeField()),
                ('mineID', models.ForeignKey(db_column='mineID', on_delete=django.db.models.deletion.CASCADE, to='setup.tblMine')),
            ],
            options={
                'db_table': 'tblCAPEX',
            },
        ),
    ]