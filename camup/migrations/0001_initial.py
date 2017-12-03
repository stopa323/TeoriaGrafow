# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-12-03 13:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField()),
                ('col', models.IntegerField()),
                ('val', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Kurs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kod_kursu', models.CharField(max_length=30)),
                ('rok', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Matrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Prefernecje_Prowadzacego',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maksymalna_ilosc_zajec_pod_rzad', models.IntegerField()),
                ('maksymalna_ilosc_cwiczen_pod_rzad', models.IntegerField()),
                ('przerwa_obiadowa_tag', models.BooleanField()),
                ('wolny_dzien_tag', models.BooleanField()),
                ('macierz_preferencji', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camup.Matrix')),
                ('prowadzacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prefernecje_Studenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kurs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camup.Kurs')),
                ('macierz_preferencji', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camup.Matrix')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kod_sali', models.CharField(max_length=30)),
                ('budynek', models.CharField(max_length=30)),
                ('ilosc_miejsc', models.IntegerField()),
                ('rzutnik_tag', models.BooleanField()),
                ('komputer_tag', models.BooleanField()),
                ('tablica_tag', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Zajecia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa_zajec', models.CharField(max_length=30)),
                ('liczba_minut_w_tygodniu', models.IntegerField()),
                ('mozliwe_sale', models.CharField(max_length=200)),
                ('Kurs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camup.Kurs')),
                ('odpowiedzialny_nauczyciel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cell',
            name='matrix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camup.Matrix'),
        ),
    ]
