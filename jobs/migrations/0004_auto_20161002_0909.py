# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='headImg',
            field=models.FileField(null=True, upload_to=b'./upload/'),
        ),
        migrations.AddField(
            model_name='author',
            name='question',
            field=models.ForeignKey(default=True, to='jobs.Question'),
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(to='jobs.Author'),
        ),
    ]
