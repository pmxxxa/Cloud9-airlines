# Generated by Django 3.0.4 on 2020-04-14 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airlines_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='city_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_from', to='airlines_app.Airport'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='city_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_to', to='airlines_app.Airport'),
        ),
    ]