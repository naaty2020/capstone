# Generated by Django 3.1 on 2020-12-25 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('negade', '0011_subscribtion'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subscribtion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscribtion',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to='negade.vendor'),
        ),
    ]
