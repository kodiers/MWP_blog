# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 17:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='users_votes',
            field=models.ManyToManyField(blank=True, related_name='post_votes', to=settings.AUTH_USER_MODEL),
        ),
    ]