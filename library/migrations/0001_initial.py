# Generated by Django 5.1.2 on 2024-11-01 19:41

import library.utils.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True)),
                ('author', models.CharField(blank=True, max_length=150, null=True)),
                ('publisher', models.CharField(blank=True, max_length=150, null=True)),
                ('publication_year', models.IntegerField(default=0)),
                ('category', models.CharField(blank=True, max_length=150, null=True)),
                ('total_quantity', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            bases=(models.Model, library.utils.mixins.UniqueSlugMixin),
        ),
    ]
