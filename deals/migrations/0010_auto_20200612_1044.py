# Generated by Django 3.0.3 on 2020-06-12 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0009_auto_20200611_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
