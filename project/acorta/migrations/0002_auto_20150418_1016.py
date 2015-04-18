# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acorta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='url_corta',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
    ]
