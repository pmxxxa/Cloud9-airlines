# Generated by Django 3.0.4 on 2020-04-15 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airlines_app', '0005_auto_20200415_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='luggage',
            name='price',
        ),
        migrations.RemoveField(
            model_name='luggage',
            name='size',
        ),
        migrations.AddField(
            model_name='luggage',
            name='booking',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='airlines_app.Booking'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='luggage',
            name='luggage_type',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='luggage',
            name='passenger',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='luggage',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CheckedInLuggage',
        ),
    ]
