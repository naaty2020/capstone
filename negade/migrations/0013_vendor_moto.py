# Generated by Django 3.1 on 2020-12-25 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('negade', '0012_auto_20201225_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='moto',
            field=models.TextField(null=True),
        ),
    ]