# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-01-07 02:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import otree.currency
import otree.db.models
import otree_save_the_change.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('otree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('amount_offered', otree.db.models.CurrencyField(choices=[(otree.currency.Currency('0'), otree.currency.Currency('0')), (otree.currency.Currency('1000'), otree.currency.Currency('1000')), (otree.currency.Currency('2000'), otree.currency.Currency('2000')), (otree.currency.Currency('3000'), otree.currency.Currency('3000')), (otree.currency.Currency('4000'), otree.currency.Currency('4000')), (otree.currency.Currency('5000'), otree.currency.Currency('5000')), (otree.currency.Currency('6000'), otree.currency.Currency('6000')), (otree.currency.Currency('7000'), otree.currency.Currency('7000')), (otree.currency.Currency('8000'), otree.currency.Currency('8000')), (otree.currency.Currency('9000'), otree.currency.Currency('9000')), (otree.currency.Currency('10000'), otree.currency.Currency('10000'))], null=True)),
                ('offer_accepted', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ult1_2_group', to='otree.Session')),
            ],
            options={
                'db_table': 'ult1_2_group',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_payoff', otree.db.models.CurrencyField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_gbat_arrived', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('_gbat_grouped', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('is_exception', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ult1_2.Group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ult1_2_player', to='otree.Participant')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ult1_2_player', to='otree.Session')),
            ],
            options={
                'db_table': 'ult1_2_player',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ult1_2_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'ult1_2_subsession',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.AddField(
            model_name='player',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ult1_2.Subsession'),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ult1_2.Subsession'),
        ),
    ]