# Generated by Django 3.0.8 on 2020-08-14 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20200813_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appstorereview',
            name='author',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='appstorereview',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appstorereview',
            name='version',
            field=models.CharField(max_length=15),
        ),
    ]