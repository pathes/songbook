# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-09-17 19:38
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
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('modification_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('modification_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('performer', models.CharField(blank=True, max_length=255)),
                ('composer', models.CharField(blank=True, max_length=255)),
                ('genre', models.CharField(blank=True, max_length=255)),
                ('year', models.CharField(blank=True, max_length=4)),
                ('confirmed', models.BooleanField(default=False)),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Songlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('modification_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('is_public', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SonglistItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='songbook.Song')),
                ('songlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='songbook.Songlist')),
            ],
        ),
        migrations.AddField(
            model_name='songlist',
            name='songs',
            field=models.ManyToManyField(through='songbook.SonglistItem', to='songbook.Song'),
        ),
    ]