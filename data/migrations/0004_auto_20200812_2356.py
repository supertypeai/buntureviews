# Generated by Django 3.0.8 on 2020-08-12 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20200812_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watch_lists', to='data.Customer'),
        ),
    ]
