# Generated by Django 3.0.3 on 2020-02-23 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0002_auto_20200223_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='expires',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='valid_from',
            field=models.DateField(blank=True, null=True),
        ),
    ]
