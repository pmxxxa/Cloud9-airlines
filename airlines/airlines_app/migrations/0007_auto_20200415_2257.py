# Generated by Django 3.0.4 on 2020-04-15 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airlines_app', '0006_auto_20200415_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='luggage',
            name='passenger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airlines_app.Passenger'),
        ),
    ]
