# Generated by Django 5.1.2 on 2024-11-09 20:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_author_publisher_loan_observation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='library.author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='library.publisher'),
        ),
    ]